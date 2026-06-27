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
    parser.add_argument(
        '--text-output', '-t',
        default='my_mutual_fund_nav.txt',
        help='Optional text file to save the printed table output.'
    )
    args = parser.parse_args()

    scheme_codes = parse_scheme_codes(args.file)
    if not scheme_codes:
        print(f'No valid scheme codes found in {args.file}')
        return

    nav_results = fetch_navs(scheme_codes)

    # Column widths
    code_width = 12
    name_width = 55
    nav_width = 12
    date_width = 14

    header = f"{'Scheme Code':<{code_width}}  {'Scheme Name':<{name_width}}  {'NAV':<{nav_width}}  {'Date':<{date_width}}"
    separator = f"{'-' * code_width}  {'-' * name_width}  {'-' * nav_width}  {'-' * date_width}"

    table_lines = [header, separator]
    for result in nav_results:
        code = result['scheme_code']
        name = result['scheme_name']
        nav = result['nav']
        date = result['last_updated']

        if len(name) > name_width:
            name = name[:name_width - 3] + '...'

        table_lines.append(
            f"{code:<{code_width}}  {name:<{name_width}}  {nav:<{nav_width}}  {date:<{date_width}}"
        )

    print('\n'.join(table_lines))

    with open(args.output, 'w', encoding='utf-8') as out_file:
        json.dump(nav_results, out_file, indent=2, ensure_ascii=False)

    with open(args.text_output, 'w', encoding='utf-8') as text_file:
        text_file.write('\n'.join(table_lines) + '\n')

    print(f'NAV results saved to {args.output}')
    print(f'Table output saved to {args.text_output}')


if __name__ == '__main__':
    main()
