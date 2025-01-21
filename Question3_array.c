#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

#define MAX_WORD_LEN 100
// adjust hash table size according to memory limit.
#define TABLE_SIZE   2000  

// structure to hold a single entry in the open-addressed hash table.
typedef struct {
    char *word;    
    int  count;    
    int  in_use;   
} HashItem;

// djb2 hash function: a common string hash attributed to Dan Bernstein.
static unsigned int djb2_hash(const char *str) {
    unsigned long hash = 5381;
    int c;
    while ((c = (unsigned char)*str++)) {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    return (unsigned int)hash;
}

// insert or update 'word' in the open-addressed hash table with linear probing.
// if 'word' already exists, increment its count.
// therwise, find an empty slot (in_use == 0) and put a new item there.

static void hash_insert(HashItem *table, int size, const char *word) {
    unsigned int hval = djb2_hash(word);
    int index = (int)(hval % size);

    for (int i = 0; i < size; i++) {
        int probe_index = (index + i) % size;
        if (!table[probe_index].in_use) {
            // found an empty slot and insert a new item. 
            table[probe_index].word   = strdup(word);
            table[probe_index].count  = 1;
            table[probe_index].in_use = 1;
            return;
        } else {
            // slot is occupied then check if it's the same word.
            if (strcmp(table[probe_index].word, word) == 0) {
                table[probe_index].count++;
                return;
            }
        }
    }

    // if we get here, the table is full. 
    fprintf(stderr, "Warning: hash table is full, cannot insert '%s'\n", word);
}

// used with qsort to compare pointers to HashItem by descending count.
static int compare_desc(const void *a, const void *b) {
    const HashItem *itemA = *(const HashItem **)a;
    const HashItem *itemB = *(const HashItem **)b;
    return (itemB->count - itemA->count); 
}


// reads words from a file, builds an open-addressed hash table (size TABLE_SIZE),
// then returns an array of the top 'n' frequent words (heap-allocated).

char **extract_top_n_words(const char *filename, int32_t n) {
    // allocate the hash table. 
    HashItem *hashTable = (HashItem *)calloc(TABLE_SIZE, sizeof(HashItem));
    if (!hashTable) {
        fprintf(stderr, "Error: could not allocate hash table.\n");
        return NULL;
    }

    // Open the file. 
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        free(hashTable);
        return NULL;
    }

    // read words, insert into the hash table. 
    char buffer[MAX_WORD_LEN];
    while (fscanf(fp, "%99s", buffer) == 1) {
        /* Convert to lowercase. */
        for (int i = 0; buffer[i]; i++) {
            buffer[i] = (char)tolower((unsigned char)buffer[i]);
        }
        hash_insert(hashTable, TABLE_SIZE, buffer);
    }
    fclose(fp);

    // collect all used items into a pointer array for sorting. 
    // first count how many items are in_use. 
    int total_items = 0;
    for (int i = 0; i < TABLE_SIZE; i++) {
        if (hashTable[i].in_use) {
            total_items++;
        }
    }

    // allocate array of pointers to HashItem.
    HashItem **item_ptrs = (HashItem **)malloc(total_items * sizeof(HashItem *));
    if (!item_ptrs) {
        fprintf(stderr, "Error: could not allocate item_ptrs.\n");
        free(hashTable);
        return NULL;
    }

    // fill the pointer array.
    int idx = 0;
    for (int i = 0; i < TABLE_SIZE; i++) {
        if (hashTable[i].in_use) {
            item_ptrs[idx++] = &hashTable[i];
        }
    }

    // sort this array by descending count. 
    qsort(item_ptrs, total_items, sizeof(HashItem *), compare_desc);

    // allocate output array of strings for the top n words. 
    char **results = (char **)malloc(n * sizeof(char *));
    if (!results) {
        fprintf(stderr, "Error: could not allocate results array.\n");
        free(item_ptrs);
        free(hashTable);
        return NULL;
    }

    // copy top n words (or fewer if total_items < n). 
    int limit = (total_items < n) ? total_items : n;
    for (int i = 0; i < limit; i++) {
        results[i] = strdup(item_ptrs[i]->word);
    }

    free(item_ptrs);
    free(hashTable); 

    return results;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <filename> <n>\n", argv[0]);
        return 1;
    }
    const char *filename = argv[1];
    int32_t top_n = atoi(argv[2]);
    if (top_n <= 0) {
        fprintf(stderr, "Error: n must be a positive integer.\n");
        return 1;
    }

    char **top_words = extract_top_n_words(filename, top_n);
    if (!top_words) {
        fprintf(stderr, "Could not open or process '%s'.\n", filename);
        return 1;
    }
    
    printf("Top %d words in '%s':\n", top_n, filename);
    for (int i = 0; i < top_n; i++) {
        if (top_words[i]) {
            printf("%2d) %s\n", i + 1, top_words[i]);
            free(top_words[i]);
        }
    }
    free(top_words);

    return 0;
}