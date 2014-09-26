## WKPD Project design thoughts

 1. Store data in flat files; move to database as part of a later process.
 1. Since we don't want to bombard server, time the roundtrip: compose request, send request, receive data, process and store data. The Wikipedia article on [Bot best practices](https://en.wikipedia.org/wiki/Wikipedia:Creating_a_bot#Bot_best_practices) (accessed 20140926) suggests "limit the total requests (read and write requests together) to no more than 10/minute."
 1. Use raw kanji for file names, not %-delimited hex names — greater readability, but slight processing delay.
 1. Files:
   2. scraped dictionary of synonyms: one dict to file, named by source file;
   2. links to request: single file, one unique link per line;
   2. links already requested: single file, one unique link per line and date requested;
   2. links to pages listing new pages: one unique link per line; to be used if "to request" list gets sparse.

[end]

