# DataTune Nashville 2027 — CFP draft

**Status:** Submitted November 13, 2026 (Sessionize title: **Data as AI Guardrail**); awaiting decision  
**Event:** DataTune Nashville, March 12–13, 2027  
**CFP deadline:** November 15, 2026  
**Submission:** https://www.datatuneconf.com/speak.html  
**Audience:** Data engineers, analytics engineers, data platform practitioners  
**Proposed length:** 60 minutes  
**Original talk:** [Data as an AI Guardrail](talk.md)  
**Existing related CFP:** [Ontologies as Inference Models](cfp-dpe-summit.md)

## Title

Data as an AI Guardrail: Using Ontologies to Ground Agentic AI

## Abstract

An AI system cannot reliably produce accurate, domain-grounded answers from inaccurate, incomplete, or misleading information. Yet we spend enormous effort improving models and prompts while overlooking the data that determines what they can know. Enterprises already have years of curated, validated data, business rules, and domain knowledge. How do we actually make that information available to agents in a form they can reason over and check?

Raw retrieval is not enough. A model may read a product row without knowing what its category means or which relationships and constraints make an assertion valid. Ontologies provide a formal semantic model: shared definitions, relationships, and inference rules. They do more than document business vocabulary. They let us test claims against the structure of the domain.

This session shows how data engineering becomes a practical AI guardrail. We will walk from controlled vocabularies and taxonomies to ontologies and knowledge graphs, then trace an agent that proposes an assertion, calls a validation tool, and rejects or corrects a claim that conflicts with the modeled domain. We will distinguish what semantic validation can prove from what still requires external factual verification.

The central point: if we want more reliable AI output, we have to engineer and validate the information it relies on. Data engineers already know how to do that work.

## Takeaways

- Why the quality and accuracy of information supplied to an AI system constrain the quality of its output.
- Why raw data retrieval is insufficient without definitions, relationships, and semantic constraints.
- How to build from controlled vocabulary through taxonomy and ontology to a populated knowledge graph.
- How ontologies work as inference models for validating agent assertions and tool interactions.
- How to place deterministic data validation into an agent workflow rather than hoping a prompt prevents hallucinations.

## Proposed 60-minute flow

1. 0–10 min: Curated enterprise data versus plausible AI hallucinations
2. 10–20 min: Why raw data and prompt rules are insufficient
3. 20–35 min: Ontology pipeline: vocabulary, taxonomies, inference, knowledge graphs
4. 35–48 min: Three implementation patterns and agent assertion validation
5. 48–55 min: Educational prerequisite example, limitations, and adoption
6. 55–60 min: Questions

## Speaker/reviewer notes

Vendor-neutral. Ground the examples in the original [slide deck](talk.md), including the educational prerequisite-checking example. Do not replace the talk with a separate access-control/governance or checkout-incident argument. Do not claim that good data mathematically guarantees perfect model output: even with accurate data, models and pipelines can still make errors.

## Post-submission notes

- Sessionize confirms the shorter submitted title **Data as AI Guardrail**. The expanded title and abstract below are the repository working version; exact submitted abstract is not confirmed.
- Two additional DataTune talks were submitted: *Shared Memory for Agents: A Wiki as a Coordination Substrate* and *Your AI Agent Does Not Have Memory: Personalization Is Governed Data Access*.

## Submission check

- Review title and abstract against the existing Data as an AI Guardrail talk.
- Confirm the CFP form's character limits and exact duration.
- Check Nashville travel against pending Barcelona March 15 CFP.
