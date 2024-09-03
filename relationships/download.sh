#!/usr/bin/env sh

# dates="
# RS_2018-01
# RS_2018-02
# RS_2018-03
# RS_2018-04
# RS_2018-05
# RS_2018-06
# RS_2018-07
# RS_2018-08
# RS_2018-09
# RS_2018-10
# RS_2018-11
# RS_2018-12
# "
dates="
RS_2018-12
RS_2018-11
RS_2018-10
"
outdir="data"
mkdir -p $outdir
for date in $dates; do
    echo $date;
    fnameout=${outdir}/${date}.jsonl.gz
    curl "https://files.pushshift.io/reddit/submissions/${date}.xz" | xz --decompress --stdout  | grep '"subreddit":"relationship_advice"' | gzip > $fnameout
done
