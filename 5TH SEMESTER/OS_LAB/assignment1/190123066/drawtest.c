#include "types.h"
#include "stat.h"
#include "user.h"

int
main(void)
{
    // declaring a buffer of 1563 bytes which can store the wolf string
    char *buf = malloc(1563);

    // ret is the value returned from sys_draw function in sysproc.c
    int ret = draw(buf, 1563);

    if (ret == -1) {
        // if size is less it gives error message
        printf(1, "ERROR: Size Too Small.\n");
    }
    else {
        //else it will print the wolfie
        printf(1, "Wolfie Size = %d Bytes\n", ret);
        printf(1, "%s\n", buf);
    }
    exit();
}
