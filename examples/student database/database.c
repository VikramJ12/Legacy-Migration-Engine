#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "database.h"
#include "utils.h"

// The actual definition of the Database struct.
struct Database {
    Student* students;
    int count;
    int capacity;
};

Database* create_database(int capacity) {
    Database* db = (Database*)malloc(sizeof(Database));
    if (!db) return NULL;
    
    db->students = (Student*)malloc(sizeof(Student) * capacity);
    if (!db->students) {
        free(db);
        return NULL;
    }
    
    db->count = 0;
    db->capacity = capacity;
    return db;
}

void free_database(Database* db) {
    if (db) {
        free(db->students);
        free(db);
    }
}

int add_student(Database* db, int id, const char* name, float gpa) {
    if (db->count >= db->capacity) {
        printf("Error: Database is full.\n");
        return -1; // Indicate failure
    }
    
    Student* s = &db->students[db->count];
    s->id = id;
    s->gpa = gpa;
    safe_strncpy(s->name, name, MAX_NAME_LEN);
    
    db->count++;
    return 0; // Indicate success
}

Student* find_student_by_id(Database* db, int id) {
    for (int i = 0; i < db->count; i++) {
        if (db->students[i].id == id) {
            return &db->students[i];
        }
    }
    return NULL; // Not found
}

void print_database(const Database* db) {
    printf("--- Student Database ---\n");
    for (int i = 0; i < db->count; i++) {
        printf("ID: %-5d | Name: %-15s | GPA: %.2f\n",
               db->students[i].id, db->students[i].name, db->students[i].gpa);
    }
    printf("------------------------\n");
}