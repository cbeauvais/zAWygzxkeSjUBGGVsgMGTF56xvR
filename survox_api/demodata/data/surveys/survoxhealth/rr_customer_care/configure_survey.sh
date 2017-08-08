#!/bin/bash

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
PATH=$PATH:$cfmcpath/go
STUDYCODE=rr_customer_care


#--------------------------------------------------------------------------------------
# build sample file
cd sample
if fonebuld fb.spx -fb.lst > fb.scr 2>&1 ; then
    echo "fonebuld built sample!"
else
    grep 'ERROR:' -fb.lst
fi
cd ..


#--------------------------------------------------------------------------------------
# copy to active directories
cp *.qff $cfmcqfl
cp sample/*.f* $cfmcfone
cp *.quo $cfmcquota

# start the server
$cfmcgo/server_start.sh $cfmcpath


#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
if [ -d setup ] ; then
    cd setup
    for spx in *.spx
    do
        nn=`echo $spx | cut -f1 -d_`
        prog=`echo $spx | cut -f2 -d_`
        lst=`echo $spx | sed -e 's/.spx/.lst/'`
        scr=`echo $spx | sed -e 's/.spx/.scr/'`
        printf "Running: $prog $spx $lst ... "
        xtra=
        if [ "$prog" = "survsupr" ] ; then
            xtra="ldev:47"
        fi
        if $prog $spx $lst $xtra > $scr 2>&1 ; then
            echo "okay"
        else
            echo "FAILED"
            grep 'ERROR' $lst
        fi
    done
    cd ..
fi

