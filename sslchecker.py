import urllib.request
import urllib.error
import queue
import sys
import ssl

domains = queue.Queue()

def enqueueDomains(filename):
    """ Open a file (denoted by @filename) and add all domains
    contained to the queue.
    """
    with open(filename, 'r') as domainz:
        for domain in domainz:
            domains.put(domain.rstrip())


def checkIfSSL(domain):
    """ Check if a particular domain supports SSL connectivity. """
    try:
        html = urllib.request.urlopen('https://' + domain).read()
        if len(html) != 0:
            return True
    except urllib.error.URLError:
        # Before we bail out, and say that the site doesn't support
        # SSL, we want to try to see if we can connect to the site
        # with a plain http connection, semantically meaning that 
        # there isn't any problem with the server itself.
        try:
            html = urllib.request.urlopen('http://' + domain).read()
            if len(html) != 0:
                return False
        except urllib.error.URLError:
            return False
    except ssl.CertificateError:
        # This happens when a domain, according to firefox at least,
        # uses an invalid certificate (my understanding is that it uses
        # a certificate issued for another domain).
        return False
        

if __name__ == '__main__':
    enqueueDomains(sys.argv[1])
    while not domains.empty():
        next_domain = domains.get()
        if next_domain is None:
            sys.exit(0)
        is_SSL = checkIfSSL(next_domain)
        with open(sys.argv[2], 'a') as results:
            print('Domain {dom} supports SSL? {support}'.format(dom=next_domain, support=is_SSL))
            results.write('Domain {dom} supports SSL? {support}\n'.format(dom=next_domain, support=is_SSL))
