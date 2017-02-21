#include <stdio.h>

define ULDATA {
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
    match(p) {
        case ULDATA[ 32, 40 ] {
            printf("hello");
        }
        case ULDATA[ 50 ] {
            printf("fooo");
        }
    }
}
