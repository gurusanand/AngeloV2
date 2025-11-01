# Low-Hanging Fruit & Pain Points Analysis
## WhatsApp Images 60-98 Review

**Date**: 2025-10-31  
**Source**: Hermes Catch-Up Meeting Transcript

---

## Image 60 - Key Discussion Points

### Context: Team discussion about query writing and testing

**Pain Points Identified:**

1. **Manual Query Writing**
   - "First of all, those five people need to write queries correctly every time, right?"
   - "Without much of a reward and then test it properly"
   - Issue: Developers manually writing queries with no automated validation

2. **Testing & Migration Complexity**
   - "All those things, right. And then migration of the code and all those things will create everything right"
   - "If if you treat the entire code. Yeah, putting dev in Dev. Right then Dev to UAT, then UAT to prod. There are two layers, right?"
   - Issue: Multi-environment deployment complexity (Dev → UAT → Prod)

3. **Incremental Mapping Changes**
   - "And then there are incremental mapping changes"
   - Issue: Handling schema evolution and mapping updates over time

4. **Business Analyst Dependency**
   - "BAs are not first time, right?"
   - "Always there is someone who has created that manually, right?"
   - Issue: Heavy reliance on BAs for initial setup

5. **Data Fetching Model Issues**
   - "And as I told you, the newer right, it's not a like to like. Yeah, in terms of modal from where we are fetching the data, it is not like to like, yeah, so th"
   - Issue: Data model mismatches between source and target

---

## Continuing analysis...

## Image 75 - 🎯 LOW-HANGING FRUIT EXPLICITLY MENTIONED!

### **CRITICAL FINDING: Specific Low-Hanging Fruit Identified**

**Direct Quote:**
> "So that is very low hanging fruit that I can think of that we can start and if can we do it in a month by using some automation."

**Context:** Discussion about server upgrades and technical debt

### Key Pain Points & Low-Hanging Fruit:

#### 1. **Server Upgrades (REL 7 to Relata)**
- **Quote**: "Right. We are moving from REL 7 to relata."
- **Issue**: Server upgrade project causing disruption
- **Scope**: Application with ~1200 jobs and 600 tables
- **Data**: Around 80 source files
- **Low-Hanging Fruit**: Automate the migration/upgrade process

#### 2. **Testing Infrastructure & Automation** ⭐ PRIMARY LOW-HANGING FRUIT
- **Quote**: "That you have readily available to test all that stuff and all those things are testing done because they are everything is like to like to like same directory structure."
- **Quote**: "Everything is there."
- **Quote**: "We we need to just create everything similar to what was earlier."
- **Issue**: Manual testing for server upgrades
- **Opportunity**: Automated testing framework since directory structure is same
- **Timeline**: Can be done in 1 month with automation

#### 3. **Java Version Compatibility Testing**
- **Quote**: "We have to test it with check all the functionality same as my Java versions are not breaking invalid and all those things."
- **Issue**: Need to validate Java version compatibility
- **Opportunity**: Automated compatibility testing suite

#### 4. **Injection Part of Tech Project**
- **Quote**: "Another thing which was a straightforward that I can think of is a project that we can take it on this our tech, that right which is injection part of it."
- **Quote**: "Oh, that. That's a tag. That part we have a server upgrades, so, Oh, OK, well there there is lot of work that we need to do."
- **Issue**: Injection component needs attention during upgrades

---


## Image 90 - 🎯 SPECIFIC 4-WEEK DELIVERY PLAN MENTIONED!

### **CRITICAL FINDING: Concrete Timeline and Deliverables**

**Direct Quote:**
> "We can create a model in four weeks."
> "Deliver it and go and with three or four feeds with it."

### Key Pain Points & Opportunities:

#### 1. **Resource Constraints & Team Overload** ⭐ MAJOR PAIN POINT
- **Quote**: "Yes. So if we are working with only one thing got, unfortunately our team works so everywhere"
- **Quote**: "Busy left, right and center. And I have 20 people just directly with me,"
- **Quote**: "I have one more person who is 20 people with them, right?"
- **Quote**: "And we are working on at a time."
- **Quote**: "Five school six projects, along with the entry support."
- **Quote**: "And all the other stuff."
- **Quote**: "Product so everyone is fully tight."
- **Issue**: Team of 40+ people spread across 5-6 projects plus support
- **Impact**: Cannot focus on innovation, firefighting mode

#### 2. **Common Model Creation Challenge** ⭐ LOW-HANGING FRUIT #2
- **Quote**: "One is pick a new file or a source and then try to create the common model in Jason is only the config"
- **Quote**: "Consolidate multiple files into one particular table and since already there's data mapping, it's not goin"
- **Quote**: "That's one lot of work. OK, that one up to the model, everything is changed."
- **Issue**: Creating common data models from multiple source files
- **Opportunity**: Automate JSON config generation for common models
- **Complexity**: Data mapping already exists, just needs consolidation

#### 3. **Upstream Dependency Constraints** ⭐ MAJOR PAIN POINT #3
- **Quote**: "We cannot use anything which is there in upstream entire construct."
- **Quote**: "Some material will come and all that. OK, perfect."
- **Quote**: "In fact, we cannot use anything of the upstream God."
- **Quote**: "Everything is new what we can do of the upstream is even the outbound log"
- **Issue**: Cannot reuse upstream components or constructs
- **Impact**: Everything must be built from scratch
- **Opportunity**: Build reusable components that don't depend on upstream

#### 4. **Proof of Concept Opportunity**
- **Timeline**: 4 weeks to create model
- **Scope**: Deliver with 3-4 feeds
- **Constraint**: Limited to 2 opportunities (not 22)
- **Reality Check**: Team bandwidth is extremely limited

---


## Image 85 - Problem Statement & Mapping Challenges

### Key Discussion Points:

#### 1. **Problem Statement Focus**
- **Quote**: "That's that's like so which problem statement that we need to focus on, Amit."
- **Quote**: "So let's say you opted 1."
- **Context**: Team trying to identify which problem to tackle first

#### 2. **Mapping Complexity Challenge**
- **Quote**: "Is there a way if we can get that map up right?"
- **Quote**: "But this is high level."
- **Quote**: "I'm not went."
- **Issue**: Need to create or obtain data mapping
- **Complexity**: High-level mapping exists but detailed mapping is missing

#### 3. **Confirmation of Server Upgrade Project** (Repeated from Image 75)
- **Quote**: "Another thing which was a straightforward that I can think of is a project that we can take it on this our tech, that right whic"
- **Quote**: "Oh, that. That's A tag. That part we have a server upgrades, so. Oh, OK, well there there is lot of work that we need to do."
- **Quote**: "During the upgrade, which point is it which server upgrade?"
- **Quote**: "Right. We are moving from REL 7 to relata."
- Confirms server upgrade is a major ongoing effort

---

