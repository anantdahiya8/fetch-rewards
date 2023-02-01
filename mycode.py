import csv
import sys
from typing import List, Dict

def spend_points(points_to_spend: int, transactions: List[Dict[str, str]]) -> Dict[str, int]:
    payer_points = {}
    transactions = sorted(transactions, key=lambda x: x['timestamp'])
    
    for transaction in transactions:
        payer = transaction['payer']
        if payer not in payer_points:
            payer_points[payer] = 0
        payer_points[payer] += int(transaction['points'])

    for key, val in payer_points.items():
        if val < 0:
            return "INVALID INPUT"

    for transaction in transactions:
        payer = transaction['payer']
        points = min(payer_points[payer], int(transaction['points']))
        if(points >= points_to_spend):
            payer_points[payer] -= points_to_spend
            points_to_spend = 0
        else:
            points_to_spend = points_to_spend - points
            payer_points[payer] -= points

        if points_to_spend == 0:
            break
    return payer_points

def read_transactions(filename: str) -> List[Dict[str, str]]:
    transactions = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)
    return transactions

if __name__ == '__main__':
    filename = 'transactions.csv'
    points_to_spend = int(sys.argv[1])
    transactions = read_transactions(filename)
    result = spend_points(points_to_spend, transactions)
    print(result)