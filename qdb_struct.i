
%inline%{

struct retval
{
    retval(void) : buffer(0), buffer_size(0) {}

    char * buffer;
    size_t buffer_size;
};

struct error_carrier
{
    error_carrier(void) : error(qdb_e_ok) {}

    qdb_error_t error;
};

%}
