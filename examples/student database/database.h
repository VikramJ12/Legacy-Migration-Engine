#ifndef DATABASE_H
#define DATABASE_H

#include "student.h"

// Forward declaration of the Database struct to hide implementation details.
// The actual definition is in database.c
typedef struct Database Database;

Database* create_database(int capacity);
void free_database(Database* db);
int add_student(Database* db, int id, const char* name, float gpa);
Student* find_student_by_id(Database* db, int id);
void print_database(const Database* db);

#endif // DATABASE_H