
import boto3
import json
from botocore.exceptions import ClientError

def check_cloudwatch_permissions():
    """Check if the current AWS credentials have the necessary CloudWatch Logs permissions."""
    required_actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
    ]
    
    try:
        # Get the current user/role
        sts_client = boto3.client('sts')
        identity = sts_client.get_caller_identity()
        print(f"AWS Identity: {json.dumps(identity, default=str)}")
        
        # Check permissions using IAM policy simulator
        iam_client = boto3.client('iam')
        
        # For IAM users
        if 'user' in identity.get('Arn', ''):
            user_name = identity['Arn'].split('/')[-1]
            try:
                response = iam_client.simulate_user_policy(
                    PolicySourceArn=identity['Arn'],
                    ActionNames=required_actions,
                    ResourceArns=[f"arn:aws:logs:*:{identity['Account']}:*"]
                )
                return _evaluate_simulation_results(response)
            except Exception as e:
                print(f"Could not simulate user policy: {str(e)}")
                return False
        
        # For roles (including Lambda execution roles)
        elif 'assumed-role' in identity.get('Arn', ''):
            print("Using an assumed role. Cannot directly check permissions.")
            print("Please ensure the role has the following permissions:")
            for action in required_actions:
                print(f"  - {action}")
            return None
        
        else:
            print("Unknown identity type. Cannot check permissions.")
            return None
            
    except ClientError as e:
        print(f"Error checking permissions: {e}")
        return False

def _evaluate_simulation_results(response):
    """Evaluate the results of the IAM policy simulation."""
    all_allowed = True
    print("\nPermission check results:")
    
    for result in response.get('EvaluationResults', []):
        action = result.get('EvalActionName')
        decision = result.get('EvalDecision')
        allowed = decision == 'allowed'
        
        if not allowed:
            all_allowed = False
            reasons = [reason.get('EvalDecisionDetail') for reason in result.get('EvalDecisionDetails', [])]
            reasons_str = ', '.join(reasons) if reasons else 'No specific reason provided'
            print(f"❌ {action}: {decision} - {reasons_str}")
        else:
            print(f"✅ {action}: {decision}")
    
    return all_allowed

if __name__ == "__main__":
    result = check_cloudwatch_permissions()
    if result is True:
        print("\n✅ All required CloudWatch Logs permissions are available.")
    elif result is False:
        print("\n❌ Missing some required CloudWatch Logs permissions.")
    else:
        print("\n⚠️ Could not determine permissions status.")
