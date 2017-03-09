# EMPL: Embedded Pattern Language in C

## A Sample

### source code
```
struct DATA {
    int dest;
    int src;
};
...
struct DATA *p;
...
%match(DATA * p) {
    [10, 20] {
        ...
    }
    [< 10, < 20] {
        ...
    }
    [_, is_good(%h)] {
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
if (p->dest == 10 && p->src == 20) {
    ...
}else if (p->dest < 10 && p->src < 20) {
    ...
}else if (is_good(p->src)) {
    ...
}
```

## Installation

EMPL requires textX, Jinja2, gcc.

```
pip install textX
pip install Jinja2
```

## Usage

```
python emplc.py [empl file]
```

It will generate c code to stdout.


