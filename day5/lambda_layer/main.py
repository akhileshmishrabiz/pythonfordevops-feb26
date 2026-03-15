import json
import pandas as pd

def lambda_handler(event, context):
    # Create a sample DataFrame
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000, 60000, 75000]
    }
    df = pd.DataFrame(data)
    
    # Perform some operation
    avg_salary = df['salary'].mean()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Lambda function executed successfully',
            'average_salary': avg_salary,
            'total_employees': len(df)
        })
    }