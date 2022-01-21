#include "list.h"

struct List* var_init(init_args args) {
    int size_out = args.size? args.size : 0;
    return create_list_base(size_out);
}

struct List* create_list_base(const int size) {
    struct List* list = (struct List*)malloc(sizeof(struct List));
    list->append = append;
    list->clear = clear;
    list->get = get;
    list->at = at;
    list->set = set;

    if (size >= 1) {
        struct ListNode* node = list->root = (struct ListNode*)malloc(sizeof(struct ListNode));

        for(int i = 1; i < size; i++)
            node = node->next = (struct ListNode*)malloc(sizeof(struct ListNode));
        
        list->end = node;
    }

    list->size = size;

    return list;
}

void append(struct List* restrict self, void* restrict value) {
    if (self->size > 0)
        self->end = self->end->next = (struct ListNode*)malloc(sizeof(struct ListNode));
    else
        self->end = self->root = (struct ListNode*)malloc(sizeof(struct ListNode));
    
    self->end->value = value;

    self->size++;
}

void clear(struct List* restrict self) {
    struct ListNode* node = self->root;

    while (node) {
        struct ListNode* next = node->next;
        free(node);
        node = next;
    }

    self->size = 0;
}

struct ListNode* get(struct List* restrict self, const int index) {
    if (!(0 <= index < self->size))
        return NULL;

    struct ListNode* node = self->root;

    for (int i = 1; i <= index; i++)
        node = node->next;

    return node;
}

void* at(struct List* restrict self, const int index) {
    struct ListNode* node = self->get(self, index);
    return node ? node->value : NULL;
}

void set(struct List* restrict self, const int index, void** restrict value) {
    struct ListNode* node = self->get(self, index);
    if (node)
        node->value = *value;
}