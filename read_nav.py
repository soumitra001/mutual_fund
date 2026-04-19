import argparse
import json
import re

from mftool import Mftool


def parse_scheme_codes(file_path):
    codes = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            text = line.strip()
            if not text:
                continue

            # Handle tab-separated or space-separated lines like:
            # 125350	Axis Small Cap Fund
            parts = re.split(r"[\t,]+", text, maxsplit=1)
            candidate = parts[0].strip()

            if candidate.lower().startswith('scheme'):
                continue

            match = re.match(r'^(\d+)', candidate)
            if match:
                codes.append(match.group(1))
    return codes


def fetch_navs(scheme_codes):
    mf = Mftool()
    results = []

    for code in scheme_codes:
        try:
            data = mf.get_scheme_quote(code)
            results.append({
                'scheme_code': code,
                'scheme_name': data.get('scheme_name', 'N/A'),
                'nav': data.get('nav', 'N/A'),
                'last_updated': data.get('last_updated', 'N/A'),
            })
        except Exception as exc:
            results.append({
                'scheme_code': code,
                'scheme_name': 'ERROR',
                'nav': 'ERROR',
                'last_updated': str(exc),
            })
    return results


def main():
    parser = argparse.ArgumentParser(description='Read scheme codes from a file and print NAV for each.')
    parser.add_argument(
        '--file', '-f',
        default='my_mutual_fund.txt',
        help='Path to the input file containing mutual fund scheme codes.'
    )
    parser.add_argument(
        '--output', '-o',
        default='my_mutual_fund_nav.json',
        help='Optional JSON file to save NAV results.'
    )
    args = parser.parse_args()

    scheme_codes = parse_scheme_codes(args.file)
    if not scheme_codes:
        print(f'No valid scheme codes found in {args.file}')
        return

    nav_results = fetch_navs(scheme_codes)

    for result in nav_results:
        print(
            f"Code: {result['scheme_code']} | "
            f"Name: {result['scheme_name']} | "
            f"NAV: {result['nav']} | "
            f"Date: {result['last_updated']}"
        )

    with open(args.output, 'w', encoding='utf-8') as out_file:
        json.dump(nav_results, out_file, indent=2, ensure_ascii=False)

    print(f'NAV results saved to {args.output}')


if __name__ == '__main__':
    main()
