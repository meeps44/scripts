# FLOW_LABEL_0=0 #(decimal), 0 hex
# 0000 00000000 11111111:
# FLOW_LABEL_1=255 #(decimal), FF hex
# 0000 11111111 00000000:
# FLOW_LABEL_2=65280 #(decimal), FF00 hex
# 1111 00000000 00000000:
# FLOW_LABEL_3=983040 #(decimal), F0000 hex
# 1111 11111111 11111111:
# FLOW_LABEL_4=1048575 #(decimal), FFFFF hex


query_result = traceroute_stats.query('`Outgoing Flow Label` == 0 and \
                       (\
                       (`Hop Flow Label` != 0 and `Hop IP`.notnull()) | \
                       (`Hop Flow Label.1` != 0 and `Hop IP.1`.notnull()) | \
                       (`Hop Flow Label.2` != 0 and `Hop IP.2`.notnull()) | \
                       (`Hop Flow Label.3` != 0 and `Hop IP.3`.notnull()) | \
                       (`Hop Flow Label.4` != 0 and `Hop IP.4`.notnull()) | \
                       (`Hop Flow Label.5` != 0 and `Hop IP.5`.notnull()) | \
                       (`Hop Flow Label.6` != 0 and `Hop IP.6`.notnull()) | \
                       (`Hop Flow Label.7` != 0 and `Hop IP.7`.notnull()) | \
                       (`Hop Flow Label.8` != 0 and `Hop IP.8`.notnull()) | \
                       (`Hop Flow Label.9` != 0 and `Hop IP.9`.notnull()) | \
                       (`Hop Flow Label.10` != 0 and `Hop IP.10`.notnull()) | \
                       (`Hop Flow Label.11` != 0 and `Hop IP.11`.notnull()) | \
                       (`Hop Flow Label.12` != 0 and `Hop IP.12`.notnull()) | \
                       (`Hop Flow Label.13` != 0 and `Hop IP.13`.notnull()) | \
                       (`Hop Flow Label.14` != 0 and `Hop IP.14`.notnull()) | \
                       (`Hop Flow Label.15` != 0 and `Hop IP.15`.notnull()) | \
                       (`Hop Flow Label.16` != 0 and `Hop IP.16`.notnull()) | \
                       (`Hop Flow Label.17` != 0 and `Hop IP.17`.notnull()) | \
                       (`Hop Flow Label.18` != 0 and `Hop IP.18`.notnull()) | \
                       (`Hop Flow Label.19` != 0 and `Hop IP.19`.notnull()) | \
                       (`Hop Flow Label.20` != 0 and `Hop IP.20`.notnull()) | \
                       (`Hop Flow Label.21` != 0 and `Hop IP.21`.notnull()) | \
                       (`Hop Flow Label.22` != 0 and `Hop IP.22`.notnull()) | \
                       (`Hop Flow Label.23` != 0 and `Hop IP.23`.notnull()) | \
                       (`Hop Flow Label.24` != 0 and `Hop IP.24`.notnull()) | \
                       (`Hop Flow Label.25` != 0 and `Hop IP.25`.notnull()) | \
                       (`Hop Flow Label.26` != 0 and `Hop IP.26`.notnull()) | \
                       (`Hop Flow Label.27` != 0 and `Hop IP.27`.notnull()) | \
                       (`Hop Flow Label.28` != 0 and `Hop IP.28`.notnull()) | \
                       (`Hop Flow Label.29` != 0 and `Hop IP.29`.notnull()) | \
                       (`Hop Flow Label.30` != 0 and `Hop IP.30`.notnull()) | \
                       (`Hop Flow Label.31` != 0 and `Hop IP.31`.notnull()) | \
                       (`Hop Flow Label.32` != 0 and `Hop IP.32`.notnull()) | \
                       (`Hop Flow Label.33` != 0 and `Hop IP.33`.notnull()) | \
                       (`Hop Flow Label.34` != 0 and `Hop IP.34`.notnull()) \
                      )', engine='python')
query_result = traceroute_stats.query('`Outgoing Flow Label` == 255 and \
                       (\
                       (`Hop Flow Label` != 255 and `Hop IP`.notnull()) | \
                       (`Hop Flow Label.1` != 255 and `Hop IP.1`.notnull()) | \
                       (`Hop Flow Label.2` != 255 and `Hop IP.2`.notnull()) | \
                       (`Hop Flow Label.3` != 255 and `Hop IP.3`.notnull()) | \
                       (`Hop Flow Label.4` != 255 and `Hop IP.4`.notnull()) | \
                       (`Hop Flow Label.5` != 255 and `Hop IP.5`.notnull()) | \
                       (`Hop Flow Label.6` != 255 and `Hop IP.6`.notnull()) | \
                       (`Hop Flow Label.7` != 255 and `Hop IP.7`.notnull()) | \
                       (`Hop Flow Label.8` != 255 and `Hop IP.8`.notnull()) | \
                       (`Hop Flow Label.9` != 255 and `Hop IP.9`.notnull()) | \
                       (`Hop Flow Label.10` != 255 and `Hop IP.10`.notnull()) | \
                       (`Hop Flow Label.11` != 255 and `Hop IP.11`.notnull()) | \
                       (`Hop Flow Label.12` != 255 and `Hop IP.12`.notnull()) | \
                       (`Hop Flow Label.13` != 255 and `Hop IP.13`.notnull()) | \
                       (`Hop Flow Label.14` != 255 and `Hop IP.14`.notnull()) | \
                       (`Hop Flow Label.15` != 255 and `Hop IP.15`.notnull()) | \
                       (`Hop Flow Label.16` != 255 and `Hop IP.16`.notnull()) | \
                       (`Hop Flow Label.17` != 255 and `Hop IP.17`.notnull()) | \
                       (`Hop Flow Label.18` != 255 and `Hop IP.18`.notnull()) | \
                       (`Hop Flow Label.19` != 255 and `Hop IP.19`.notnull()) | \
                       (`Hop Flow Label.20` != 255 and `Hop IP.20`.notnull()) | \
                       (`Hop Flow Label.21` != 255 and `Hop IP.21`.notnull()) | \
                       (`Hop Flow Label.22` != 255 and `Hop IP.22`.notnull()) | \
                       (`Hop Flow Label.23` != 255 and `Hop IP.23`.notnull()) | \
                       (`Hop Flow Label.24` != 255 and `Hop IP.24`.notnull()) | \
                       (`Hop Flow Label.25` != 255 and `Hop IP.25`.notnull()) | \
                       (`Hop Flow Label.26` != 255 and `Hop IP.26`.notnull()) | \
                       (`Hop Flow Label.27` != 255 and `Hop IP.27`.notnull()) | \
                       (`Hop Flow Label.28` != 255 and `Hop IP.28`.notnull()) | \
                       (`Hop Flow Label.29` != 255 and `Hop IP.29`.notnull()) | \
                       (`Hop Flow Label.30` != 255 and `Hop IP.30`.notnull()) | \
                       (`Hop Flow Label.31` != 255 and `Hop IP.31`.notnull()) | \
                       (`Hop Flow Label.32` != 255 and `Hop IP.32`.notnull()) | \
                       (`Hop Flow Label.33` != 255 and `Hop IP.33`.notnull()) | \
                       (`Hop Flow Label.34` != 255 and `Hop IP.34`.notnull()) \
                      )', engine='python')
query_result = traceroute_stats.query('`Outgoing Flow Label` == 65280 and \
                       (\
                       (`Hop Flow Label` != 65280 and `Hop IP`.notnull()) | \
                       (`Hop Flow Label.1` != 65280 and `Hop IP.1`.notnull()) | \
                       (`Hop Flow Label.2` != 65280 and `Hop IP.2`.notnull()) | \
                       (`Hop Flow Label.3` != 65280 and `Hop IP.3`.notnull()) | \
                       (`Hop Flow Label.4` != 65280 and `Hop IP.4`.notnull()) | \
                       (`Hop Flow Label.5` != 65280 and `Hop IP.5`.notnull()) | \
                       (`Hop Flow Label.6` != 65280 and `Hop IP.6`.notnull()) | \
                       (`Hop Flow Label.7` != 65280 and `Hop IP.7`.notnull()) | \
                       (`Hop Flow Label.8` != 65280 and `Hop IP.8`.notnull()) | \
                       (`Hop Flow Label.9` != 65280 and `Hop IP.9`.notnull()) | \
                       (`Hop Flow Label.10` != 65280 and `Hop IP.10`.notnull()) | \
                       (`Hop Flow Label.11` != 65280 and `Hop IP.11`.notnull()) | \
                       (`Hop Flow Label.12` != 65280 and `Hop IP.12`.notnull()) | \
                       (`Hop Flow Label.13` != 65280 and `Hop IP.13`.notnull()) | \
                       (`Hop Flow Label.14` != 65280 and `Hop IP.14`.notnull()) | \
                       (`Hop Flow Label.15` != 65280 and `Hop IP.15`.notnull()) | \
                       (`Hop Flow Label.16` != 65280 and `Hop IP.16`.notnull()) | \
                       (`Hop Flow Label.17` != 65280 and `Hop IP.17`.notnull()) | \
                       (`Hop Flow Label.18` != 65280 and `Hop IP.18`.notnull()) | \
                       (`Hop Flow Label.19` != 65280 and `Hop IP.19`.notnull()) | \
                       (`Hop Flow Label.20` != 65280 and `Hop IP.20`.notnull()) | \
                       (`Hop Flow Label.21` != 65280 and `Hop IP.21`.notnull()) | \
                       (`Hop Flow Label.22` != 65280 and `Hop IP.22`.notnull()) | \
                       (`Hop Flow Label.23` != 65280 and `Hop IP.23`.notnull()) | \
                       (`Hop Flow Label.24` != 65280 and `Hop IP.24`.notnull()) | \
                       (`Hop Flow Label.25` != 65280 and `Hop IP.25`.notnull()) | \
                       (`Hop Flow Label.26` != 65280 and `Hop IP.26`.notnull()) | \
                       (`Hop Flow Label.27` != 65280 and `Hop IP.27`.notnull()) | \
                       (`Hop Flow Label.28` != 65280 and `Hop IP.28`.notnull()) | \
                       (`Hop Flow Label.29` != 65280 and `Hop IP.29`.notnull()) | \
                       (`Hop Flow Label.30` != 65280 and `Hop IP.30`.notnull()) | \
                       (`Hop Flow Label.31` != 65280 and `Hop IP.31`.notnull()) | \
                       (`Hop Flow Label.32` != 65280 and `Hop IP.32`.notnull()) | \
                       (`Hop Flow Label.33` != 65280 and `Hop IP.33`.notnull()) | \
                       (`Hop Flow Label.34` != 65280 and `Hop IP.34`.notnull()) \
                      )', engine='python')
query_result = traceroute_stats.query('`Outgoing Flow Label` == 983040 and \
                       (\
                       (`Hop Flow Label` != 983040 and `Hop IP`.notnull()) | \
                       (`Hop Flow Label.1` != 983040 and `Hop IP.1`.notnull()) | \
                       (`Hop Flow Label.2` != 983040 and `Hop IP.2`.notnull()) | \
                       (`Hop Flow Label.3` != 983040 and `Hop IP.3`.notnull()) | \
                       (`Hop Flow Label.4` != 983040 and `Hop IP.4`.notnull()) | \
                       (`Hop Flow Label.5` != 983040 and `Hop IP.5`.notnull()) | \
                       (`Hop Flow Label.6` != 983040 and `Hop IP.6`.notnull()) | \
                       (`Hop Flow Label.7` != 983040 and `Hop IP.7`.notnull()) | \
                       (`Hop Flow Label.8` != 983040 and `Hop IP.8`.notnull()) | \
                       (`Hop Flow Label.9` != 983040 and `Hop IP.9`.notnull()) | \
                       (`Hop Flow Label.10` != 983040 and `Hop IP.10`.notnull()) | \
                       (`Hop Flow Label.11` != 983040 and `Hop IP.11`.notnull()) | \
                       (`Hop Flow Label.12` != 983040 and `Hop IP.12`.notnull()) | \
                       (`Hop Flow Label.13` != 983040 and `Hop IP.13`.notnull()) | \
                       (`Hop Flow Label.14` != 983040 and `Hop IP.14`.notnull()) | \
                       (`Hop Flow Label.15` != 983040 and `Hop IP.15`.notnull()) | \
                       (`Hop Flow Label.16` != 983040 and `Hop IP.16`.notnull()) | \
                       (`Hop Flow Label.17` != 983040 and `Hop IP.17`.notnull()) | \
                       (`Hop Flow Label.18` != 983040 and `Hop IP.18`.notnull()) | \
                       (`Hop Flow Label.19` != 983040 and `Hop IP.19`.notnull()) | \
                       (`Hop Flow Label.20` != 983040 and `Hop IP.20`.notnull()) | \
                       (`Hop Flow Label.21` != 983040 and `Hop IP.21`.notnull()) | \
                       (`Hop Flow Label.22` != 983040 and `Hop IP.22`.notnull()) | \
                       (`Hop Flow Label.23` != 983040 and `Hop IP.23`.notnull()) | \
                       (`Hop Flow Label.24` != 983040 and `Hop IP.24`.notnull()) | \
                       (`Hop Flow Label.25` != 983040 and `Hop IP.25`.notnull()) | \
                       (`Hop Flow Label.26` != 983040 and `Hop IP.26`.notnull()) | \
                       (`Hop Flow Label.27` != 983040 and `Hop IP.27`.notnull()) | \
                       (`Hop Flow Label.28` != 983040 and `Hop IP.28`.notnull()) | \
                       (`Hop Flow Label.29` != 983040 and `Hop IP.29`.notnull()) | \
                       (`Hop Flow Label.30` != 983040 and `Hop IP.30`.notnull()) | \
                       (`Hop Flow Label.31` != 983040 and `Hop IP.31`.notnull()) | \
                       (`Hop Flow Label.32` != 983040 and `Hop IP.32`.notnull()) | \
                       (`Hop Flow Label.33` != 983040 and `Hop IP.33`.notnull()) | \
                       (`Hop Flow Label.34` != 983040 and `Hop IP.34`.notnull()) \
                      )', engine='python')
query_result = traceroute_stats.query('`Outgoing Flow Label` == 1048575 and \
                       (\
                       (`Hop Flow Label` != 1048575 and `Hop IP`.notnull()) | \
                       (`Hop Flow Label.1` != 1048575 and `Hop IP.1`.notnull()) | \
                       (`Hop Flow Label.2` != 1048575 and `Hop IP.2`.notnull()) | \
                       (`Hop Flow Label.3` != 1048575 and `Hop IP.3`.notnull()) | \
                       (`Hop Flow Label.4` != 1048575 and `Hop IP.4`.notnull()) | \
                       (`Hop Flow Label.5` != 1048575 and `Hop IP.5`.notnull()) | \
                       (`Hop Flow Label.6` != 1048575 and `Hop IP.6`.notnull()) | \
                       (`Hop Flow Label.7` != 1048575 and `Hop IP.7`.notnull()) | \
                       (`Hop Flow Label.8` != 1048575 and `Hop IP.8`.notnull()) | \
                       (`Hop Flow Label.9` != 1048575 and `Hop IP.9`.notnull()) | \
                       (`Hop Flow Label.10` != 1048575 and `Hop IP.10`.notnull()) | \
                       (`Hop Flow Label.11` != 1048575 and `Hop IP.11`.notnull()) | \
                       (`Hop Flow Label.12` != 1048575 and `Hop IP.12`.notnull()) | \
                       (`Hop Flow Label.13` != 1048575 and `Hop IP.13`.notnull()) | \
                       (`Hop Flow Label.14` != 1048575 and `Hop IP.14`.notnull()) | \
                       (`Hop Flow Label.15` != 1048575 and `Hop IP.15`.notnull()) | \
                       (`Hop Flow Label.16` != 1048575 and `Hop IP.16`.notnull()) | \
                       (`Hop Flow Label.17` != 1048575 and `Hop IP.17`.notnull()) | \
                       (`Hop Flow Label.18` != 1048575 and `Hop IP.18`.notnull()) | \
                       (`Hop Flow Label.19` != 1048575 and `Hop IP.19`.notnull()) | \
                       (`Hop Flow Label.20` != 1048575 and `Hop IP.20`.notnull()) | \
                       (`Hop Flow Label.21` != 1048575 and `Hop IP.21`.notnull()) | \
                       (`Hop Flow Label.22` != 1048575 and `Hop IP.22`.notnull()) | \
                       (`Hop Flow Label.23` != 1048575 and `Hop IP.23`.notnull()) | \
                       (`Hop Flow Label.24` != 1048575 and `Hop IP.24`.notnull()) | \
                       (`Hop Flow Label.25` != 1048575 and `Hop IP.25`.notnull()) | \
                       (`Hop Flow Label.26` != 1048575 and `Hop IP.26`.notnull()) | \
                       (`Hop Flow Label.27` != 1048575 and `Hop IP.27`.notnull()) | \
                       (`Hop Flow Label.28` != 1048575 and `Hop IP.28`.notnull()) | \
                       (`Hop Flow Label.29` != 1048575 and `Hop IP.29`.notnull()) | \
                       (`Hop Flow Label.30` != 1048575 and `Hop IP.30`.notnull()) | \
                       (`Hop Flow Label.31` != 1048575 and `Hop IP.31`.notnull()) | \
                       (`Hop Flow Label.32` != 1048575 and `Hop IP.32`.notnull()) | \
                       (`Hop Flow Label.33` != 1048575 and `Hop IP.33`.notnull()) | \
                       (`Hop Flow Label.34` != 1048575 and `Hop IP.34`.notnull()) \
                      )', engine='python')
#query_result.to_csv('E:\\test.csv', encoding='utf-8')
my_df = query_result[['Outgoing Flow Label',
                      'Hop Flow Label',
                      'Hop Flow Label.1',
                      'Hop Flow Label.2',
                      'Hop Flow Label.3',
                      'Hop Flow Label.4',
                      'Hop Flow Label.5',
                      'Hop Flow Label.6',
                      'Hop Flow Label.7',
                      'Hop Flow Label.8',
                      'Hop Flow Label.9',
                      'Hop Flow Label.10',
                      'Hop Flow Label.11',
                      'Hop Flow Label.12',
                      'Hop Flow Label.13',
                      'Hop Flow Label.14',
                      'Hop Flow Label.15',
                      'Hop Flow Label.16',
                      'Hop Flow Label.17',
                      'Hop Flow Label.18',
                      'Hop Flow Label.19',
                      'Hop Flow Label.20',
                      'Hop Flow Label.21',
                      'Hop Flow Label.22',
                      'Hop Flow Label.23',
                      'Hop Flow Label.24',
                      'Hop Flow Label.25',
                      'Hop Flow Label.26',
                      'Hop Flow Label.27',
                      'Hop Flow Label.28',
                      'Hop Flow Label.29',
                      'Hop Flow Label.30',
                      'Hop Flow Label.31',
                      'Hop Flow Label.32',
                      'Hop Flow Label.33',
                      'Hop Flow Label.34'
                      ]]
my_df.to_csv('E:\\test.csv', encoding='utf-8')
