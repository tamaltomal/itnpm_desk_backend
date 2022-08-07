# datetime.strptime(date_str, '%I:%M %d %B %Y')
# date_only = full_line[14:]
# re.search('DVTP[N]?\d{1,4}', tunnel_3)
# f'absolute end {(datetime.now() + timedelta(days=7)).strftime("%I:%M %d %B %Y")}'

To get the list of all tunnel Group
# tunnels = Tunnel.objects.all()
To get the policies of a tunnel
# tunnel.policies.all()


To get the list of Policy
# policies = Policy.objects.all()
To get the tunnels of a policy
# policy.tunnel_set.all()


Input: datetime.now().strftime("%I%M%S%d%B%Y")
Output: '12385031July2022'