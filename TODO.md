# TODO
(A) Establish persistence events with SQL backend
(B) Better enforce multi-tenancy (Have some kind of check for users to access their data)
(C) Implement error handle within GET request for security of running code
(D) Implement pagination into users filter to better break down the fields
(E) Sort GET results by fields by most recent login attempts
(F) Add more endpoints for analytics or enriching events with threat score

#### Future Additions
(A) Add encryption for sensitive info within columns and have decryption only within application memory
(B) Add admin role to allow modification of data using PUT/DELETE operations
(C) Push real-time suspicious logins to dashboards
(D) Add exportation of login summaries through CSV or JSON's