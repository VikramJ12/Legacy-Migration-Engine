#include <stdio.h>
#include "database.h"
#include "student.h" 

int main() {
    printf("Initializing student database system...\n");
    Database* db = create_database(10); // Capacity of 10 students

    if (!db) {
        fprintf(stderr, "Failed to create database.\n");
        return 1;
    }

    // Add some students
    add_student(db, 101, "Alice", 3.8f);
    add_student(db, 102, "Bob", 3.5f);
    add_student(db, 103, "Charlie", 4.0f);

    // Print the entire database
    print_database(db);

    // Find a specific student
    int id_to_find = 102;
    printf("\nSearching for student with ID %d...\n", id_to_find);
    Student* found_student = find_student_by_id(db, id_to_find);

    if (found_student) {
        printf("Found Student -> ID: %d, Name: %s, GPA: %.2f\n",
               found_student->id, found_student->name, found_student->gpa);
    } else {
        printf("Student with ID %d not found.\n", id_to_find);
    }

    // Clean up
    free_database(db);
    printf("\nDatabase system shut down.\n");

    return 0;
}