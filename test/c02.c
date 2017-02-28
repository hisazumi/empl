#include <stdio.h>

struct PACKET_TYPE {
    int a;
    int b;
};

struct ULDATA {
    uint32 dest;
    uint32 src;
    uint32 fid;
    uint8 htl;
    uint8 ackn;
    uint8 retryn;
    PACKET_TYPE pt;
    uint1 loop_flag;
    uint32 header_size;
};

int main() {
    %match(ULDATA * p) {
        case [ b, c, d, e, f, g, [a, b] ] {
            printf("hello");
        }
        case [ 50 ] {
            printf("fooo");
        }
    }
}
