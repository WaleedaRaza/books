# BookPDFOpener - Quick Start Guide

## 🚀 Getting Started

### 1. Initialize Next.js Project
```bash
npx create-next-app@latest bookpdfopener --typescript --tailwind --app
cd bookpdfopener
```

### 2. Install Core Dependencies
```bash
# LangChain & AI
npm install langchain @langchain/openai @langchain/community
npm install langgraph

# UI Components
npm install shadcn-ui
npx shadcn-ui@latest init

# Database
npm install @vercel/postgres
npm install @vercel/kv  # For Redis

# Auth
npm install next-auth

# Utilities
npm install zod  # Validation
npm install date-fns  # Date handling
```

### 3. Project Structure
```
bookpdfopener/
├── app/
│   ├── (auth)/
│   │   └── login/
│   ├── (dashboard)/
│   │   ├── dashboard/
│   │   ├── lists/
│   │   └── search/
│   ├── api/
│   │   ├── search/
│   │   ├── lists/
│   │   └── pdf-discovery/
│   └── layout.tsx
├── components/
│   ├── ui/          # shadcn components
│   ├── BookCard.tsx
│   ├── PDFLink.tsx
│   ├── ListManager.tsx
│   └── SearchResults.tsx
├── lib/
│   ├── langchain/
│   │   ├── agents/
│   │   │   └── pdf-discovery-agent.ts
│   │   ├── workflows/
│   │   │   └── pdf-discovery-workflow.ts
│   │   └── prompts/
│   │       └── pdf-discovery-prompts.ts
│   ├── search/
│   │   ├── duckduckgo.ts
│   │   ├── archive-org.ts
│   │   └── scoring.ts
│   ├── db/
│   │   └── schema.ts
│   └── utils/
├── types/
│   └── index.ts
└── public/
```

### 4. Environment Variables (.env.local)
```env
# OpenAI (for LangChain)
OPENAI_API_KEY=your_key_here

# Database
POSTGRES_URL=your_vercel_postgres_url
POSTGRES_PRISMA_URL=your_prisma_url
POSTGRES_URL_NON_POOLING=your_non_pooling_url

# Redis (optional, for caching)
KV_URL=your_vercel_kv_url

# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_secret_here

# App
NODE_ENV=development
```

### 5. Core Agent Implementation (lib/langchain/agents/pdf-discovery-agent.ts)
```typescript
import { ChatOpenAI } from "@langchain/openai";
import { AgentExecutor, createOpenAIFunctionsAgent } from "langchain/agents";
import { Tool } from "@langchain/core/tools";

export class PDFDiscoveryAgent {
  private llm: ChatOpenAI;
  private agent: AgentExecutor;

  constructor() {
    this.llm = new ChatOpenAI({
      modelName: "gpt-4-turbo-preview",
      temperature: 0.3,
    });

    const tools = [
      new Tool({
        name: "search_duckduckgo",
        description: "Search DuckDuckGo for PDF links",
        func: this.searchDuckDuckGo.bind(this),
      }),
      new Tool({
        name: "score_pdf_quality",
        description: "Score PDF quality and reliability",
        func: this.scorePDFQuality.bind(this),
      }),
    ];

    this.agent = new AgentExecutor({
      agent: createOpenAIFunctionsAgent({
        llm: this.llm,
        tools,
        prompt: this.getSystemPrompt(),
      }),
      tools,
      verbose: true,
    });
  }

  private getSystemPrompt() {
    return `You are an expert at finding free, legal PDFs of books online.
    
    Your goal: Find the best quality PDFs for each book.
    
    Strategy:
    1. Generate optimal search queries
    2. Search multiple sources
    3. Score each result
    4. Validate correctness
    5. Return top 3-5 results
    
    Prioritize direct PDF files and reliable sources like Archive.org.`;
  }

  async discoverPDFs(book: { title: string; author: string }) {
    const result = await this.agent.invoke({
      input: `Find PDFs for: "${book.title}" by ${book.author}`,
    });
    return result;
  }

  private async searchDuckDuckGo(query: string) {
    // Use ddgs package (from current script)
    // Return search results
  }

  private async scorePDFQuality(url: string, book: Book) {
    // Use scoring logic from current script
    // Return score and reasoning
  }
}
```

### 6. API Route (app/api/pdf-discovery/route.ts)
```typescript
import { NextRequest, NextResponse } from "next/server";
import { PDFDiscoveryAgent } from "@/lib/langchain/agents/pdf-discovery-agent";

export async function POST(request: NextRequest) {
  try {
    const { title, author } = await request.json();
    
    const agent = new PDFDiscoveryAgent();
    const results = await agent.discoverPDFs({ title, author });
    
    return NextResponse.json({ success: true, results });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: "Failed to discover PDFs" },
      { status: 500 }
    );
  }
}
```

### 7. Frontend Component (components/SearchResults.tsx)
```typescript
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function SearchResults({ book }: { book: Book }) {
  const [pdfs, setPdfs] = useState<PDFLink[]>([]);
  const [loading, setLoading] = useState(false);

  const searchPDFs = async () => {
    setLoading(true);
    const res = await fetch("/api/pdf-discovery", {
      method: "POST",
      body: JSON.stringify({
        title: book.title,
        author: book.author,
      }),
    });
    const data = await res.json();
    setPdfs(data.results);
    setLoading(false);
  };

  return (
    <div>
      <Button onClick={searchPDFs} disabled={loading}>
        {loading ? "Searching..." : "Find PDFs"}
      </Button>
      
      {pdfs.map((pdf) => (
        <Card key={pdf.id}>
          <a href={pdf.url} target="_blank">
            {pdf.url}
          </a>
          <span>Confidence: {pdf.confidence}%</span>
        </Card>
      ))}
    </div>
  );
}
```

---

## 🎯 MVP Checklist

- [ ] Next.js project setup
- [ ] LangChain agent basic implementation
- [ ] DuckDuckGo search integration
- [ ] PDF scoring system (from current script)
- [ ] Basic UI (book search, results display)
- [ ] List upload/parsing
- [ ] Database schema
- [ ] Auth setup
- [ ] Deploy to Vercel

---

## 📚 Key Files to Port from Current Script

1. **Scoring Logic** → `lib/search/scoring.ts`
2. **PDF Detection** → `lib/search/pdf-detection.ts`
3. **Domain Filtering** → `lib/search/domain-filter.ts`
4. **Logging System** → `lib/utils/logging.ts`

---

## 🚀 Deployment

1. Push to GitHub
2. Connect to Vercel
3. Set environment variables
4. Deploy!

---

Ready to build! 🎉



