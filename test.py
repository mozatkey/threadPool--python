import os
import getopt, sys
import traceback


__help_string_ = '''
Usage timer [OPTION] ...
    -c, --config=CONFIG_FILE                       the configure file to load
    -P  --path=PATH                                path for nginx install
    -n  --num=NUMBER                               number for curl tries
    -m, --max_peer_failed=MAX_PEER_FAILED          max_peer_failed
    -h, --help                                     print this help infomation and exit
'''


def restart(conf, path, max_peer_failed):
    '''restart the nginx with our own configure'''
    cur_path =  os.getcwd()
    command = "%s/sbin/nginx -c %s/conf/%s  >/dev/null"%(path, cur_path, conf)
    print command
    os.system( "killall -9 nginx" )
    os.system( "export MAX_PEER_FAILED=%s"%max_peer_failed )
    os.system( command )

def curl_test(curl_times):
    for i in range(int(curl_times)):
      # print i
      #os.system( "curl http://localhost:8000/%d >> curl_result 2>/dev/null"%i )
      os.system( "curl http://localhost:8000/%d >> curl_result 2>/dev/null"%i )

def get_result(path, max_peer_failed):
    '''get result of this test'''
    log = "%s/logs/error.log"%path

    c_pc_tries    = '''grep "pc->tries" %s |awk '{print (%s-$NF)}' |sort|uniq  -c>>result'''%(log, int(max_peer_failed)+1)
    c_rnode_index = '''grep "rnode index" %s |awk '{print $NF}'|sort |uniq -c|awk '{print $1, $2}'>>result '''%log
    print c_pc_tries
    print c_rnode_index
    os.system( c_pc_tries  )
    os.system( c_rnode_index )
    c_sum_pc_tries = ''' grep -v port result |awk '{sum+=$1} END {print "sum_pc_tries = ", sum}' '''
    c_sum_rnode_touched = ''' grep port result |awk '{sum+=$1} END {print "sum_rnode_touched = ", sum}'  '''
    c_pc_failed = ''' grep "The page is temporarily unavailable" curl_result|awk '{sum+=1} END {print "sum_pc_failed= ", sum}' '''
    os.system( c_sum_pc_tries )
    os.system( c_sum_rnode_touched )
    os.system( c_pc_failed )
    os.system("cat result")

def clear_all(path):
    ''' clear  log'''
    os.system( ">%s/logs/error.log"%path )
    os.system( ">curl_result" )
    os.system( ">result" )

def test_main(conf, path, max_peer_failed, curl_times):
    '''test main function for nginx consistent_hash '''
    restart(conf, path, max_peer_failed)
    curl_test(curl_times)
    get_result(path, max_peer_failed)
    clear_all(path)


if __name__ == "__main__":
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'c:m:h:p:n:', ['config=',
                                     'path', 'max_peer_failed=', 'help', 'num'])
        conf = None
        path = None
        max_peer_failed = None
        curl_times = None

        #print opts
        for o, a in opts:
            if o == '-h' or o == '--help':
                print __help_string_
                exit()
            if o == '-c' or o == '--config':
                conf = a
            if o == '-p' or o == '--path':
                path = a
                print a
            if o == '-n' or o == '--num':
                curl_times = a
                print a
            if o == '-m' or o == '--max_peer_failed':
                max_peer_failed = a

        if conf == None or path == None or max_peer_failed == None or curl_times == None:
            print __help_string_
        else:
            print conf, path, max_peer_failed, curl_times
            test_main(conf, path, max_peer_failed, curl_times)

    except getopt.GetoptError:
        #traceback.print_exc(file=sys.stdout)
        print __help_string_


