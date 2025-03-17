#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <emmintrin.h>
#include <stdint.h>
#include <windows.h>
#include <tlhelp32.h>

static PyObject* scan_chunk(PyObject* self, PyObject* args) {
    const char* memory_chunk;
    Py_ssize_t memory_chunk_len;
    const uint8_t* pattern;
    Py_ssize_t pattern_len;
    const uint8_t* mask;
    uint64_t base_address;
    int chunk_offset;
    uint64_t offset1 = 0x17A4;
    uint64_t offset2 = 0x5EA0;
    uint64_t offset3 = 0x4;

    if (!PyArg_ParseTuple(args, "y#y#y#KI", &memory_chunk, &memory_chunk_len, &pattern, &pattern_len, &mask, &pattern_len, &base_address, &chunk_offset)) {
        return NULL;
    }

    PyObject* result = PyList_New(0);
    __m128i pattern_vector, mask_vector, chunk_vector, masked_pattern, masked_chunk;
    int simd_iterations = (int)(pattern_len / 16);
    int remaining_bytes = (int)(pattern_len % 16);

    for (Py_ssize_t i = 0; i <= memory_chunk_len - pattern_len; i++) {
        int match = 1;

        for (int j = 0; j < simd_iterations; j++) {
            pattern_vector = _mm_loadu_si128((__m128i*)(pattern + j * 16));
            mask_vector = _mm_loadu_si128((__m128i*)(mask + j * 16));
            chunk_vector = _mm_loadu_si128((__m128i*)(memory_chunk + i + j * 16));

            masked_pattern = _mm_and_si128(pattern_vector, mask_vector);
            masked_chunk = _mm_and_si128(chunk_vector, mask_vector);

            __m128i cmp_result = _mm_cmpeq_epi8(masked_pattern, masked_chunk);

            if (_mm_movemask_epi8(cmp_result) != 0xFFFF) {
                match = 0;
                break;
            }
        }

        if (match && remaining_bytes > 0) {
            for (int j = simd_iterations * 16; j < pattern_len; j++) {
                if ((memory_chunk[i + j] & mask[j]) != (pattern[j] & mask[j])) {
                    match = 0;
                    break;
                }
            }
        }

        if (match) {
            uint64_t address1 = base_address + chunk_offset + i + offset1;
            uint64_t address2 = address1 + offset2;
            uint64_t address3 = address1 + offset3;

            PyObject* values_list = PyList_New(0);
            PyList_Append(values_list, PyLong_FromUnsignedLongLong(address2));
            PyList_Append(values_list, PyLong_FromUnsignedLongLong(address1));
            PyList_Append(values_list, PyLong_FromUnsignedLongLong(address3));

            PyList_Append(result, values_list);
            Py_DECREF(values_list);
        }
    }

    return result;
}

typedef struct {
    void* baseAddress;
    size_t regionSize;
} MemoryRegion;

MemoryRegion* get_memory_regions(const char* process_name, int* count) {
    MemoryRegion* memoryRegions = NULL;
    *count = 0;

    DWORD processID = 0;
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Failed to create snapshot\n");
        return NULL;
    }

    PROCESSENTRY32 processEntry = { 0 };
    processEntry.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(snapshot, &processEntry)) {
        do {
            if (strcmp(process_name, processEntry.szExeFile) == 0) {
                processID = processEntry.th32ProcessID;
                break;
            }
        } while (Process32Next(snapshot, &processEntry));
    }
    CloseHandle(snapshot);

    if (processID == 0) {
        fprintf(stderr, "Process not found\n");
        return NULL;
    }

    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processID);
    if (!hProcess) {
        fprintf(stderr, "Failed to open process\n");
        return NULL;
    }

    MEMORY_BASIC_INFORMATION mbi;
    unsigned char* addr = NULL;

    while (VirtualQueryEx(hProcess, addr, &mbi, sizeof(mbi)) == sizeof(mbi)) {
        if (mbi.State == MEM_COMMIT && !(mbi.Protect & PAGE_NOACCESS)) {
            MemoryRegion* temp = realloc(memoryRegions, (*count + 1) * sizeof(MemoryRegion));
            if (temp == NULL) {
                fprintf(stderr, "Memory allocation failed\n");
                free(memoryRegions);
                CloseHandle(hProcess);
                return NULL;
            }
            memoryRegions = temp;
            memoryRegions[*count].baseAddress = mbi.BaseAddress;
            memoryRegions[*count].regionSize = mbi.RegionSize;
            (*count)++;
        }
        addr += mbi.RegionSize;
    }

    CloseHandle(hProcess);
    return memoryRegions;
}

static PyObject* get_regions(PyObject* self, PyObject* args) {
    const char* process_name;
    unsigned long long region_size;

    if (!PyArg_ParseTuple(args, "sK", &process_name, &region_size)) {
        return NULL;
    }

    int count = 0;
    MemoryRegion* regions = get_memory_regions(process_name, &count);

    for (int i = 0; i < count; i++) {
        if (regions[i].regionSize == region_size) {
            void* baseAddress = regions[i].baseAddress;
            free(regions);
            return PyLong_FromVoidPtr(baseAddress);
        }
    }

    free(regions);
    Py_RETURN_NONE;
}

static PyMethodDef MyMethods[] = {
    {"get_regions", get_regions, METH_VARARGS, "Get memory region base address."},
    {"scan_chunk", scan_chunk, METH_VARARGS, "Scan a memory chunk for a pattern."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef scanmodule = {
    PyModuleDef_HEAD_INIT,
    "scanmodule",
    NULL,
    -1,
    MyMethods
};

PyMODINIT_FUNC PyInit_scanmodule(void) {
    return PyModule_Create(&scanmodule);
}
