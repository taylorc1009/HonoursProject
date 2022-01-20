#include "list.h"

#define INFINITY 7654321

struct Node {
    int number;
    int x;
    int y;
    int demand;
    int ready_time;
    int due_date;
    int service_duration;
};

struct Destination {
    float arrival_time;
    float departure_time;
    float wait_time;
    struct Node* node;
};

struct Vehicle {
    float current_capacity;
    float route_distance;
    struct List* destinations;
};

struct Solution {
    float total_distance;
    float distance_unbalance;
    float cargo_unbalance;
    struct List* vehicles;
};