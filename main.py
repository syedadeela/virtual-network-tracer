import dpkt
import socket
import pygeoip

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def main():
    f = open('wire.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '''<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
    <Style id="transBluePoly">
    <LineStyle>
    <width>1.5</width>
    <color>501400E6</color>
    </LineStyle>
    </Style>'''
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print(kmldoc)

def plotIPs(pcap):
    kmlPts = ''
    india_coordinates = [
        (77.2090, 28.6139),   # New Delhi
        (72.8777, 19.0760),   # Mumbai
        (77.5946, 12.9716),   # Bangalore
        (74.8204, 34.1306),   # Zakura
        (74.7661, 34.2244),   # Ganderbal
        (75.5337, 32.3666),   # Kathua
        (74.7973, 34.0837),   # Srinagar
        (74.8570, 32.7266)    # Jammu
    ]
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src, india_coordinates)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts

def retKML(dstip, srcip, india_coordinates):
    dst = gi.record_by_name(dstip)
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        kml = ''
        for longitude, latitude in india_coordinates:
            kml += (
                '<Placemark>\n'
                '<name>%s to %s</name>\n'
                '<extrude>1</extrude>\n'
                '<tessellate>1</tessellate>\n'
                '<styleUrl>#transBluePoly</styleUrl>\n'
                '<LineString>\n'
                '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
                '</LineString>\n'
                '</Placemark>\n'
            )%(srcip, dstip, dstlongitude, dstlatitude, longitude, latitude)
        return kml
    except:
        return ''

if __name__ == '__main__':
    main()
