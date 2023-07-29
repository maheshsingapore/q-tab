Most organizations have a url dictionary in some form or shape.
 
Users can add/ modify this dictionary themselves, so a single addition by a user can benefit everyone else.
 
However, looking at this from an organizational perspective, following is a repetitive use case for users of a url dictionary.
 
Use case:
 
User looking for a JIRA ticket, say jira123.
 
1) User looks up and clicks on jira url
2) User searches for jira123
 
Another use case:
 
User looking for details on a host hostname123.
1) User looks up and clicks on inventory application
2) User searches for hostname123
 
The catch here is that for most (if not all) users, jira123 can only mean a jira ticket that should be viewed in JIRA.
Similarly, there would be individual identifiers that related to a particular application.
 
The bigger idea here is associating a pattern with a url ONCE, and letting a third party/ common dictionary handle the redirection instead of users figuring this out themselves on EVERY search.
 
Q-Tab is a humble try to address this problem.
 
Where the pattern is has a unique match in the redirect dictionary, Q-Tab should redirect users to the corresponding url (equivalent of Google's "I am feeling lucky")
When the pattern matches multiples entries in the redirect dictionary, Q-Tab will present a list of pre-populated redirect urls.
 
This works well for most users, where we have a common definition for most internal systems.
In the event there are multiple matches for a pattern, Q-Tab will provide a list of pre-populated urls:
 
One-time setup for Q-Tab:
 
1) Navigate to Chrome Settings
2) Click on "Manage Search Engines"
3) Add a new search engine "Q-Tab", keyword as "q" and the following URL (remember to substitute your user ID in the below URL)
 
Searching using Q-Tab:
 
1) In the chrome omnibox (address bar), hit q + tab.
2) Enter jira123, hit enter.
 
So, whats the benefit?
 
1) More efficient search
2) Ability to define url redirection on a firm level - a single redirect definition can benefit others in the firm
3) No need of bookmarks. When in doubt, use Q-Tab.