#!/usr/bin/env sh


# https://earlyvoting.texas-election.com/Elections/getElectionEVDates.do

for day in `seq -w 4 30`; do

    curl 'https://earlyvoting.texas-election.com/Elections/downloadVoterInfoReport.do' \
      -H 'authority: earlyvoting.texas-election.com' \
      -H 'pragma: no-cache' \
      -H 'cache-control: no-cache' \
      -H 'origin: https://earlyvoting.texas-election.com' \
      -H 'upgrade-insecure-requests: 1' \
      -H 'dnt: 1' \
      -H 'content-type: application/x-www-form-urlencoded' \
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36' \
      -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
      -H 'sec-fetch-site: same-origin' \
      -H 'sec-fetch-mode: navigate' \
      -H 'sec-fetch-user: ?1' \
      -H 'sec-fetch-dest: document' \
      -H 'referer: https://earlyvoting.texas-election.com/Elections/getEVDetails.do' \
      -H 'accept-language: en-US,en;q=0.9' \
      -H 'cookie: JSESSIONID=CC938D92AA4D10A342E9B47297FA8562.ports-01; __cfduid=d5105bc323439c023b3621fc2c8377bf01604343591' \
      --data-raw 'idElection=44144&selectedDate=2020-10-'$day'+00%3A00%3A00.0&idTown=' \
      --compressed > data_texas/earlyvoting_2020-10-$day.csv

done
