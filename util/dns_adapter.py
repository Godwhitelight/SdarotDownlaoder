from urllib.parse import urlparse, ParseResult
from requests.adapters import HTTPAdapter
from dns.resolver import Resolver, NXDOMAIN


class HostHeaderSSLAdapter(HTTPAdapter):
    def resolve(self, host):
        dns_resolver = Resolver()
        dns_resolver.nameservers = [
            # '208.67.222.222',  # OpenDNS
            '8.8.8.8'          # Google
        ]
        try:
            answers = dns_resolver.resolve(host, 'A')
        except NXDOMAIN:
            return host

        for rdata in answers:
            return str(rdata)

    def send(self, request, **kwargs):
        connection_pool_kwargs = self.poolmanager.connection_pool_kw

        result: ParseResult = urlparse(request.url)
        resolved_ip = self.resolve(result.hostname)

        if result.scheme == 'https' and resolved_ip:
            request.url = request.url.replace(
                f'https://{result.hostname}',
                f'https://{resolved_ip}',
            )
            connection_pool_kwargs['server_hostname'] = result.hostname
            connection_pool_kwargs['assert_hostname'] = result.hostname

            request.headers['Host'] = result.hostname
        else:
            connection_pool_kwargs.pop('server_hostname', None)
            connection_pool_kwargs.pop('assert_hostname', None)

        return super(HostHeaderSSLAdapter, self).send(request, **kwargs)

