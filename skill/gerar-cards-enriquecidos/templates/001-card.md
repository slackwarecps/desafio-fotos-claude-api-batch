Scenario: Developer Productivity with Claude You are building developer productivity tools using the Claude Agent SDK. The agent helps engineers explore unfamiliar codebases, understand legacy systems, generate boilerplate code, and automate repetitive tasks. It uses built-in tools (Read, Write, Bash, Edit) with MCP servers. A team wants to add a "cancel renewal" workflow to a legacy subscription service. The initial implementation point is unclear because cancellation behavior appears split across command-line scripts, web handlers, and scheduled jobs. In earlier similar tasks, immediate edits repeatedly targeted the wrong abstraction and had to be rolled back after tests exposed broken shared behavior. Which workflow should the tool recommend first?

---

[ ] A - Instruct Claude to read every repository file first, then implement changes in the same extended session.
[ ] B - Proceed with direct execution, relying on test failures to reveal hidden dependencies and guide successive corrective edits.
[ ] C - Start separate direct-execution sessions for each suspected module, then manually combine the resulting edits later.
[ ] D - Use plan mode to map relevant flows and compare implementation points before allowing file modifications.