# The Determinism Boundary: Where Probabilistic Inference Ends and Deterministic Enforcement Begins

Remember the first time you typed a prompt and the model did exactly what you wanted? It felt like magic. Humans are bad communicators. We leave out half of what we mean and expect everyone else to fill in the blanks. LLMs are remarkably good at doing exactly that: interpreting ambiguous requests, inferring intent, and navigating missing information. Now when you type you probably get complete garbage, and wondered why it suddenly couldn't read your mind. Usually we were very specific the first time and started assuming the model would just know the rest.

We make that same assumption about the rules of our businesses. We know who can approve a refund, which customer records are private, and what counts as a bad idea in production. It feels obvious to us, so we forget that none of it is automatically obvious to an agent. And unlike a coworker who knows the organization, the model is inferring what we meant from whatever context we happened to give it.

That is where a useful property of LLMs becomes a dangerous assumption. Just because a model can infer an action from a user's intent does not mean it should determine whether the action is allowed. We call the separation between probabilistic inference and enforceable authorization the Determinism Boundary. The model figures out what the user is trying to accomplish and proposes a next step. The system establishes what is actually permitted.

## Probabilistic Systems Are Good at Questions With Multiple Possible Answers

Suppose you ask an agent to resolve a customer's billing problem. A refund might fix it, but so might a credit, a corrected invoice, or an escalation to support. The agent has to figure out what the customer probably meant, inspect what information it can access, and infer a sensible next step. This is the kind of ambiguity models are good at handling. We want that flexibility.

Now suppose the agent decides a $2,000 refund would make everybody happy. Can the employee on whose behalf it is acting approve that refund? That's not something we should ask the model to guess. The answer depends on the employee's identity, the account, the refund amount, and the company's rules. The model may have inferred a perfectly reasonable solution to the customer's problem. That still does not give it authority to issue the refund.

There is a funny real-world illustration of this. Remember when people convinced a Chevrolet dealership chatbot to agree to sell a vehicle for $1? [Business Insider covered the exchange](https://www.businessinsider.com/car-dealership-chevrolet-chatbot-chatgpt-pranks-chevy-2023-12). Nobody actually bought a new Chevy for a dollar. The chatbot just generated the words. But that's precisely the point: saying "deal" is one thing; being authorized to make a deal is another. If that chatbot had been able to complete a real transaction, the pricing and approval rules would have needed to live in the system executing the sale, not in the chatbot's interpretation of the conversation.

## Prompts Are Not Enforcement

You can tell a model not to reveal payroll data. You can put a $500 refund limit in the system prompt. You can tell it to ask for confirmation before deleting an account. All of those instructions are useful. None of them actually establishes access control. They tell the model what behavior you want, not what the connected systems will permit.

This is something we've talked about on Domesticating AI. Co-host Matt Sharp has discussed prompt hacking, including in ["How to Hack an Agent in 10 Prompts"](https://thedatapioneer.substack.com/p/how-to-hack-an-agent-in-10-prompts). The uncomfortable thing about prompts is that, when it comes to enforcement, they're a bit like the more guidelines than hard rules. You can put an instruction at the beginning, repeat it at the end, or write it in capital letters. It's still language being interpreted by a probabilistic model, and other language can influence that interpretation.

![](https://tenor.com/view/code-guidelines-pirates-code-captain-barbosa-pirates-of-the-caribbean-gif-14292102)

We've been through a version of this engineering lesson before with SQL injection. We didn't make databases safe by writing a very stern note asking everyone not to submit malicious queries. We changed how applications treat untrusted input and enforce access. Prompt injection is a different technical problem, but the principle still applies: if a rule really matters, the model's ability to remember or interpret it cannot be the thing keeping it true.

## The Boundary Exists Before Execution

There are really two ways this goes wrong, and they are easy to mix together. One is the agent *doing something* it shouldn't: issuing a refund, deleting an account, changing a production configuration, or sending a message it had no authority to send. The other is the agent *seeing something* it shouldn't: pulling payroll data, a private customer record, or an internal document that the person asking the question isn't authorized to read. One is an unauthorized action. The other can become a data leak before any visible action happens.

The first requires enforceable rules about tools and business operations. Who can perform this action? On which resource? Under what conditions? Is there a spending limit or an approval step? The second requires enforceable data-access rules during search, retrieval, and connector calls. If I ask an agent about a customer's invoice, the retrieval system needs to establish which invoices I'm allowed to see before handing them to the model. Fetching every invoice and putting "please don't reveal the private ones" in the prompt is not a security architecture.

This also connects back to the Context Void from our earlier essays. We spend a lot of time asking whether an agent has the right information to complete the task. There is another question we have to ask first: is this information actually allowed to be part of its context? A document can be relevant and still be off-limits. A tool can be useful and still be unauthorized. Better retrieval doesn't solve that distinction on its own.

## The Model Proposes; Infrastructure Enforces

One of the useful things to understand about tool-calling models is that they don't reach into your systems and execute code by force of will. They generate a structured request that the surrounding application may choose to execute. That gives us a natural place to enforce rules. The model can infer that a customer invoice is worth fetching; the system still has to check whether that invoice may be returned to this user.

It's the same story with the refund. Figuring out that a refund would help is inference. Enforcing who may issue it, for how much, and on which account is infrastructure. We don't need a philosophical debate with the model about whether the refund is a good idea. We need the business rule to hold whether the model is brilliant, confused, or responding to a malicious prompt.

## We Could Have Engineered for This

This is a system architecture problem that requires engineering not coazing. Instead, too many agent architectures try to turn the prompt into an employee handbook, a security policy, and a permission system all at once. Then, when the agent does something surprising, we add more instructions. There is a place for better prompting, of course. There is also a point where we need software to say no.

We should have treated permissions and action limits as infrastructure from the start. A sandbox can constrain where code runs, but it cannot, by itself, establish whether an agent is allowed to read a customer's records or issue a refund. We'll explore sandboxing in the next essay. For now, the important distinction is that a model can infer what to try, but the rules governing what it can know and do must live outside the model.

It's tempting to think this problem disappears as models get smarter. I think the opposite happens. A more capable model can find more tools, come up with more creative paths to a goal, and operate across more systems. That's exciting. It's also exactly why the boundaries need to become more explicit. A model that can find ten ways to solve a problem shouldn't be able to find an eleventh way around the organization's permissions.

## Other Companies Are Engineering a Deterministic Boundary

One thing I find encouraging is that Haikei isn't the only company engineering a deterministic boundary between an agent's inference and the permissions that govern its actions. Different teams are arriving at this from different parts of the stack, and I think that's healthy. We need more than one approach to a problem this fundamental.

I used to work at Tailscale, so this one feels particularly familiar. Access control has always been central to how I think about what Tailscale does: first establish who someone is, then enforce what they can reach. [Tailscale's Aperture](https://aperture.tailscale.com/) brings that philosophy to AI. It uses Tailscale identity and explicit, deny-by-default grants to govern access to models and MCP connector capabilities. The gateway checks the permissions; the model doesn't get to infer its way into access. Tailscale describes [how these grants work](https://tailscale.com/docs/aperture/how-grants-work). A small but important detail: deny-by-default doesn't mean a fresh installation is locked down to nothing; administrators still need to review the default grants.

Anthropic is doing something related inside Claude Code. Its managed settings let organizations enforce tool rules such as which commands or files are allowed, denied, or require approval. These rules can be distributed to developer machines as managed configuration; Claude Enterprise also supports server-managed settings distributed to signed-in clients. That's enforcement by the coding environment rather than a request for the model to remember what it is permitted to do. See the [settings reference](https://code.claude.com/docs/en/settings-reference) and [managed settings](https://code.claude.com/docs/en/managed-settings).

Aperture's gateway, Claude Code's native permission system, and Kei's editor and tenant-side enforcement paths aren't identical products. They don't all solve the same data-access or business-policy problems. But they share a direction I think matters: permissions are explicit rules enforced by infrastructure, not conclusions that an AI model is trusted to reach. The more companies we see building this way, the more normal that boundary becomes for production agents.

## What We Built to Enforce the Boundary

At Haikei, we've been intentional about the kinds of rules we enforce. In a closed application, role-based access control (RBAC) may be enough to say which roles can invoke an operation. But enterprise data is rarely that tidy. Two people with the same job title may have access to different customers, projects, or documents. In distributed systems, permissions often have to follow the person, the specific resource, and the circumstances of the request. That's why attribute-based access control (ABAC) matters. [NIST's ABAC guidance](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) explains the underlying model; the important idea here is that the access rule uses real attributes, not a permission invented by the agent.

The same principle applies to tool and business rules. An agent may infer that issuing a refund would resolve a customer issue, or that opening a file would answer a question. Neither inference should bypass an access limit. At Haikei, we separate the policy that governs an operation from the model proposing it. How enforcement happens depends on the tool environment: supported coding editors use their native permission systems; governed connector and custom-harness calls are mediated by a tenant-side runtime. If you want the architecture rather than another acronym-filled detour, we've diagrammed it on [How It Works](https://haikeilabs.com/how-it-works).

## The Determinism Boundary Is the Architectural Line

A useful agent should be free to interpret what the user wants and propose ways to accomplish it. It should not be free to expand its own access to information or its authority to change the world. Those are two different risks, which is why we need enforceable rules over both what the agent may retrieve and what it may execute.

The goal isn't to make AI less capable. It's to stop confusing capability with authority. Let the model be good at inference. Let the surrounding systems do their job of enforcing the rules. Infer probabilistically. Enforce deterministically. That's the Determinism Boundary.

## References & Further Reading

- Domesticating AI — [Hacking AI: Why Most AI Systems Are Insecure by Default](https://podfollow.com/domesticating-ai/episode/f33144ea5b3392d9479a9aba7d6dc478f76ff5d9/view) (episode on prompt injection and agent security)
- [Domesticating AI — podcast homepage](https://podcasts.apple.com/us/podcast/domesticating-ai/id1873338950)
- Matt Sharp, ["How to Hack an Agent in 10 Prompts"](https://thedatapioneer.substack.com/p/how-to-hack-an-agent-in-10-prompts)
- Haikei Labs — [How It Works](https://haikeilabs.com/how-it-works)
- Haikei Labs — [Kei PDP/PEP white paper](https://haikeilabs.com/whitepapers/policy-decision-and-enforcement.pdf)
