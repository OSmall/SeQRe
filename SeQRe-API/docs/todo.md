- [x] conglomerate into one stack named seqre- [ ]stack
- [x] windows local invoke
    - [x] With database working
- [ ] figure out CORS and add headers to all functions
- [ ] Postman testing
- [ ] Add proper error responses
- [ ] Refactor db so that primary key is not combined
- [x] Developer Guide
- [ ] API endpoint documentation with Swagger


- [] Require headers to be present. Right now if they are not present, there is an internal server error

I have decided to do staging just by running tests locally, deploying to prod then testing prod. Local API still connects to remote database, so there is some risk. I'll try and change this later