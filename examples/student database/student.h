#ifndef STUDENT_H
#define STUDENT_H

#define MAX_NAME_LEN 50

typedef struct {
    int id;
    char name[MAX_NAME_LEN];
    float gpa;
} Student;

#endif // STUDENT_H