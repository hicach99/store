from django.contrib.sessions.middleware import SessionMiddleware
import requests
from app.models import Configuration

try:
    config=Configuration.objects.all()[0]
except:
    config=None
default_rates={"MAD": 1, "AED": 0.352421, "AFN": 8.505973, "ALL": 10.312903, "AMD": 37.604224, "ANG": 0.171772, "AOA": 48.932373, "ARS": 19.523953, "AUD": 0.144707, "AWG": 0.171772, "AZN": 0.164371, "BAM": 0.177093, "BBD": 0.191924, "BDT": 10.242114, "BGN": 0.177093, "BHD": 0.036082, "BIF": 201.277682, "BMD": 0.095962, "BND": 0.129353, "BOB": 0.667956, "BRL": 0.505473, "BSD": 0.095962, "BTN": 7.933408, "BWP": 1.27658, "BYN": 0.297961, "BZD": 0.191924, "CAD": 0.131946, "CDF": 199.045571, "CHF": 0.088554, "CLP": 77.4958, "CNY": 0.661841, "COP": 457.109453, "CRC": 52.791301, "CUP": 2.303093, "CVE": 9.984064, "CZK": 2.169698, "DJF": 17.054497, "DKK": 0.675508, "DOP": 5.310419, "DZD": 13.129789, "EGP": 2.989898, "ERN": 1.439433, "ETB": 5.184867, "EUR": 0.090547, "FJD": 0.214272, "FKP": 0.079484, "FOK": 0.675508, "GBP": 0.079485, "GEL": 0.249589, "GGP": 0.079484, "GHS": 1.175117, "GIP": 0.079484, "GMD": 6.148608, "GNF": 829.036211, "GTQ": 0.753125, "GYD": 20.408339, "HKD": 0.752173, "HNL": 2.383016, "HRK": 0.682219, "HTG": 14.911854, "HUF": 36.024151, "IDR": 1478.949586, "ILS": 0.346278, "IMP": 0.079484, "INR": 7.933484, "IQD": 141.131969, "IRR": 4132.531584, "ISK": 13.52031, "JEP": 0.079484, "JMD": 14.715358, "JOD": 0.068037, "JPY": 12.739796, "KES": 12.538675, "KGS": 8.458122, "KHR": 391.212521, "KID": 0.144704, "KMF": 44.545755, "KRW": 125.673617, "KWD": 0.029638, "KYD": 0.079968, "KZT": 44.920383, "LAK": 1632.296206, "LBP": 1439.432929, "LKR": 32.4822, "LRD": 15.606637, "LSL": 1.761439, "LYD": 0.464724, "MDL": 1.799521, "MGA": 416.643503, "MKD": 5.554099, "MMK": 202.815047, "MNT": 341.654368, "MOP": 0.77472, "MRU": 3.333571, "MUR": 4.537574, "MVR": 1.490624, "MWK": 101.379256, "MXN": 1.81625, "MYR": 0.429939, "MZN": 6.191895, "NAD": 1.761439, "NGN": 44.502399, "NIO": 3.533901, "NOK": 1.030428, "NPR": 12.693453, "NZD": 0.154781, "OMR": 0.036897, "PAB": 0.095962, "PEN": 0.3665, "PGK": 0.340547, "PHP": 5.274156, "PKR": 27.30978, "PLN": 0.423806, "PYG": 693.181353, "QAR": 0.349302, "RON": 0.445449, "RSD": 10.570222, "RUB": 7.301482, "RWF": 105.74306, "SAR": 0.359858, "SBD": 0.812885, "SCR": 1.295388, "SDG": 53.627681, "SEK": 1.015865, "SGD": 0.129354, "SHP": 0.079484, "SLE": 2.060282, "SLL": 2060.281964, "SOS": 54.982564, "SRD": 3.347018, "SSP": 75.530209, "STN": 2.218379, "SYP": 245.783537, "SZL": 1.761439, "THB": 3.313476, "TJS": 1.056331, "TMT": 0.338039, "TND": 0.302731, "TOP": 0.228438, "TRY": 1.819856, "TTD": 0.655494, "TVD": 0.144704, "TWD": 2.960388, "TZS": 225.339055, "UAH": 3.55512, "UGX": 361.86787, "USD": 0.095787, "UYU": 3.801547, "UZS": 1103.087316, "VES": 2.305367, "VND": 2277.488393, "VUV": 11.595894, "WST": 0.262912, "XAF": 59.39434, "XCD": 0.259098, "XDR": 0.07187, "XOF": 59.39434, "XPF": 10.805046, "YER": 24.188697, "ZAR": 1.761462, "ZMW": 1.966367, "ZWL": 88.291667}

class DefaultSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if not request.session.get('rates'):
            try:
                url = f"https://v6.exchangerate-api.com/v6/{config.exchangerate_api}/latest/{config.currency.code}" if config else 'https://google.com'
                d = requests.get(url).json()
                if config and d["result"] == "success":
                    request.session['rates']=d["conversion_rates"]
            except Exception as e:
                request.session['rates']=default_rates
        if not 'currency' in request.session:
            request.session['currency'] = config.currency.code if config else 'MAD'