#!/usr/bin/env python3
"""Regenerate assets/ca-certificates.crt from Mozilla's certdata.txt.

Usage: assets/update-ca-certificates.py NSS_3_131_1_RTM

Downloads lib/ckfw/builtins/certdata.txt for the given NSS release tag and
writes every root that Mozilla trusts for TLS server authentication
(CKA_TRUST_SERVER_AUTH = CKT_NSS_TRUSTED_DELEGATOR) as PEM, sorted by label.
Roots trusted only for e-mail or code signing are left out, as are roots that
Mozilla has removed or distrusted. This mirrors what Debian's ca-certificates
and curl's mk-ca-bundle do.
"""
import base64
import os
import re
import sys
import textwrap
import urllib.request

URL = "https://raw.githubusercontent.com/nss-dev/nss/{tag}/lib/ckfw/builtins/certdata.txt"


def parse(text):
    objects = []
    cur = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.startswith("#") or line.startswith("BEGINDATA"):
            continue
        if line.startswith("CKA_CLASS"):
            cur = {}
            objects.append(cur)
        if cur is None:
            continue
        key, typ, val = re.match(r"^(\S+)\s+(\S+)\s*(.*)$", line).groups()
        if typ == "MULTILINE_OCTAL":
            data = bytearray()
            while not lines[i].startswith("END"):
                for o in re.findall(r"\\([0-7]{3})", lines[i]):
                    data.append(int(o, 8))
                i += 1
            i += 1
            cur[key] = bytes(data)
        elif typ == "UTF8":
            cur[key] = val.strip('"')
        else:
            cur[key] = val
    return objects


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tag = sys.argv[1]
    with urllib.request.urlopen(URL.format(tag=tag)) as r:
        objects = parse(r.read().decode("utf-8"))

    def ident(o):
        return (o["CKA_LABEL"], o["CKA_SERIAL_NUMBER"], o["CKA_ISSUER"])

    trusts = {ident(o): o for o in objects if o.get("CKA_CLASS") == "CKO_NSS_TRUST"}
    roots = []
    for c in (o for o in objects if o.get("CKA_CLASS") == "CKO_CERTIFICATE"):
        t = trusts.get(ident(c))
        if t and t.get("CKA_TRUST_SERVER_AUTH") == "CKT_NSS_TRUSTED_DELEGATOR":
            b64 = base64.b64encode(c["CKA_VALUE"]).decode()
            pem = "-----BEGIN CERTIFICATE-----\n%s\n-----END CERTIFICATE-----\n" % "\n".join(textwrap.wrap(b64, 64))
            roots.append((c["CKA_LABEL"].lower(), pem))
    roots.sort()

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ca-certificates.crt")
    with open(out, "w") as f:
        f.writelines(pem for _, pem in roots)
    print("wrote %d TLS server roots from %s to %s" % (len(roots), tag, out))


if __name__ == "__main__":
    main()
