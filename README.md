# EMPL: Embedded Pattern Language in C

## A Sample

### source code
```
%define DATA {
    int dest;
    int src;
};
...
struct DATA *p;
...
%match(p) {
    case [10, 20] {
        ...
    }
    case [< 10, < 20] {
        ...
    }
    case [_, is_good(here)] {
        ...
    }
}
```

### generated code

```
struct DATA {
    int dest;
    int src;
};
...
struct DATA *p;
...
if (p->dest == 10, p->src == 20) {
    ...
}else if (p->dest < 10 && p->src < 20) {
    ...
}else if (is_good(p->src)) {
    ...
}
```

