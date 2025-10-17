#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

typedef uint64_t ull;

// Global ops counter for fair comparisons
static ull OPS = 0;

typedef enum FibType {
    ITERATIVE = 0,
    RECURSIVE = 1,
    DP = 2,
    ALL = 3,
    ITERATIVE_DP_TOGETHER = 4
} FibType;

// ----- Recursive -----
ull fib_recursive_single(int n) {
    if (n <= 2) return 1;
    OPS++;
    return fib_recursive_single(n - 1) + fib_recursive_single(n - 2);
}

// ----- DP (Memoized) -----
// Simple memo up to n (stack-allocated for simplicity; bounds checked in caller)
ull fib_dp_single_internal(int n, ull *memo) {
    if (n <= 2) return 1;
    if (memo[n] != 0) return memo[n];
    OPS++;
    memo[n] = fib_dp_single_internal(n - 1, memo) + fib_dp_single_internal(n - 2, memo);
    return memo[n];
}

// ----- Iterative series 1..n -----
ull *fib_iterative_series(int n) {
    if (n <= 0) return NULL;
    ull *series = (ull *) malloc((n) * sizeof(ull));
    if (!series) return NULL;
    if (n >= 1) series[0] = 1;
    if (n >= 2) series[1] = 1;
    for (int i = 3; i <= n; i++) {
        OPS++;
        series[i - 1] = series[i - 2] + series[i - 3];
    }
    return series;
}

ull *fib_recursive_series(int n) {
    if (n <= 0) return NULL;
    ull *series = (ull *) malloc((n) * sizeof(ull));
    if (!series) return NULL;
    for (int i = 1; i <= n; i++) {
        series[i - 1] = fib_recursive_single(i);
    }
    return series;
}

ull *fib_dp_series(int n) {
    if (n <= 0) return NULL;
    ull *series = (ull *) malloc((n) * sizeof(ull));
    if (!series) return NULL;
    ull *memo = (ull *) calloc(n + 1, sizeof(ull));
    if (!memo) { free(series); return NULL; }
    for (int i = 1; i <= n; i++) {
        series[i - 1] = fib_dp_single_internal(i, memo);
    }
    free(memo);
    return series;
}

void print_series(ull *series, int n) {
    for (int i = 0; i < n; i++) {
        printf("%llu", (unsigned long long) series[i]);
        if (i < n - 1) printf(" ");
    }
    printf("\n");
}

double time_function_series(ull *(*func)(int), int n, bool print) {
    struct timespec begin, end;
    OPS = 0; // reset
    clock_gettime(CLOCK_MONOTONIC, &begin);
    ull *series = func(n);
    clock_gettime(CLOCK_MONOTONIC, &end);
    if (print && series) {
        print_series(series, n);
    }
    if (series) free(series);
    return (end.tv_nsec - begin.tv_nsec) / 1000000000.0 + (end.tv_sec - begin.tv_sec);
}

void help() {
    printf("./fib.out N [Type] [Print]\n");
    printf("\tN is the Fibonacci count to generate (series 1..N).\n");
    printf("\t[Type] 4=dp+iter together (CSV), 3=all (CSV), 2=dp, 1=recursive, 0=iterative, default 3.\n");
    printf("\t[Print] any third arg prints the series for non-CSV modes.\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("at least two arguments needed!\n");
        help();
        return 1;
    }

    const int n = atoi(argv[1]);
    int type = 3;
    bool print = false;
    if (argc > 2) type = atoi(argv[2]);
    if (argc > 3) print = true;

    double t;
    switch (type) {
        case ITERATIVE: {
            printf("iterative version\n");
            t = time_function_series(fib_iterative_series, n, print);
            printf("time: %f(%llu)\n", t, (unsigned long long) OPS);
            break;
        }
        case RECURSIVE: {
            printf("recursive version\n");
            t = time_function_series(fib_recursive_series, n, print);
            printf("time: %f(%llu)\n", t, (unsigned long long) OPS);
            break;
        }
        case DP: {
            printf("dynamic programming version\n");
            t = time_function_series(fib_dp_series, n, print);
            printf("time: %f(%llu)\n", t, (unsigned long long) OPS);
            break;
        }
        case ITERATIVE_DP_TOGETHER: {
            t = time_function_series(fib_iterative_series, n, false);
            printf("%f,%llu,", t, (unsigned long long) OPS);
            t = time_function_series(fib_dp_series, n, false);
            printf("%f,%llu,-,-", t, (unsigned long long) OPS);
            break;
        }
        case ALL:
        default: {
            t = time_function_series(fib_iterative_series, n, false);
            printf("%f,%llu,", t, (unsigned long long) OPS);
            t = time_function_series(fib_dp_series, n, false);
            printf("%f,%llu,", t, (unsigned long long) OPS);
            t = time_function_series(fib_recursive_series, n, false);
            printf("%f,%llu", t, (unsigned long long) OPS);
            break;
        }
    }
}


