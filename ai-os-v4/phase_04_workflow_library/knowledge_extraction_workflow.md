# Knowledge Extraction Workflow Specification

## 1. Purpose & Objective
Automate unstructured document parsing, entity-relation extraction, vector indexing, graph node creation, and knowledge base enrichment.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Raw document corpus (PDFs, Markdown, HTML), embedding model API, vector database (Milvus/Pinecone), graph DB (Neo4j).
- **Trigger Conditions**: Ingestion trigger from document upload repository.

## 3. Participating Agent Roles & Responsibilities
- **Knowledge Engineer**: Defines ontology schema, entity extraction taxonomy, and graph relationship rules.
- **NLP Specialist**: Configures chunking strategies, embedding pipeline, and NER models.
- **Information Architect**: Audits graph consistency, vector retrieval precision, and chunk deduplication.

## 4. Step-by-Step Execution Sequence

### Step 1: Document Parsing & Text Normalization
- **Inputs**: Raw document corpus, OCR engine (Tesseract/Unstructured).
- **Actions**: Extract raw text, strip formatting noise, perform OCR on image tables, split into structural sections.
- **Outputs**: Cleaned plain text / markdown files.
- **Verification**: Parsing validation check ensuring 0 empty pages or corrupted character encoding.

### Step 2: Semantic Chunking & Embedding Generation
- **Inputs**: Normalized text files, tokenizer, embedding model (text-embedding-3-large).
- **Actions**: Apply recursive semantic chunking (500 tokens with 100 token overlap), generate dense vector embeddings.
- **Outputs**: Chunk metadata records and vector arrays.
- **Verification**: Vector dimension audit matching target index configuration (e.g. 1536 dimensions).

### Step 3: Named Entity & Relation Extraction (NER/RE)
- **Inputs**: Semantic chunks, LLM extraction prompt / spaCy model, ontology schema.
- **Actions**: Extract domain entities (Concepts, Tools, APIs, Authors) and explicit relations (DEPENDS_ON, IMPLEMENTS, REQUIRES).
- **Outputs**: JSON-LD Entity-Relation triples.
- **Verification**: Schema validation check verifying all extracted entity types conform to ontology.

### Step 4: Vector & Graph Database Ingestion
- **Inputs**: Vector embeddings, E-R triples, Pinecone/Neo4j endpoints.
- **Actions**: Upsert vector embeddings with metadata into vector DB; merge nodes and edges into Neo4j graph DB.
- **Outputs**: Ingested Vector Database index and Neo4j Graph DB update status.
- **Verification**: Database query confirmation verifying node count increase.

### Step 5: Retrieval Evaluation & Index Optimization
- **Inputs**: Evaluation query set, ground truth answers, RAG Triad benchmark (Ragas).
- **Actions**: Run sample RAG queries, compute Context Precision, Context Recall, and Faithfulness metrics.
- **Outputs**: Knowledge Extraction Benchmark Report.
- **Verification**: Context Precision >= 0.85 and Context Recall >= 0.80.

## 5. Decision Gates & Branching Rules
- Gate 1: Schema validation check must pass 100% of extracted triples before Neo4j insertion.
- Gate 2: Retrieval benchmark (Ragas precision >= 0.85) required before enabling production search index.

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: PDF OCR failure on scanned table -> Action: Route document to vision LLM (GPT-4o) table parser fallback.
- Failure Mode 2: Vector embedding rate-limit exceeded -> Action: Implement exponential backoff queue with batch size reduction.

## 7. Artifact Delivery & Output Standard
Ingested Vector Index, Neo4j Knowledge Graph triples, Ragas Retrieval Benchmark Report, and Processed Corpus Manifest.
