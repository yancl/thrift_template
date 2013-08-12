include "fb303.thrift"

exception ExceptionBase {
    1: i32 what,
    2: string why
}

service Base extends fb303.FacebookService {
}
