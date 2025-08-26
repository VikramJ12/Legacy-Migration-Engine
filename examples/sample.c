struct Point {
    int x;
    int y;
};

void move(struct Point *p, int dx, int dy) {
    p->x += dx;
    p->y += dy;
}

int main() {
    struct Point p = {0, 0};
    move(&p, 3, 4);
    printf("%d %d\n", p.x, p.y);
    return 0;
}
