



struct blah { char *b_data; };

void set_bh_page(struct blah *bh, unsigned long offset)
{
        if ((1UL << 12 ) <= offset)
                __builtin_trap() ;
        bh->b_data = (char *)offset;
}
