#!/usr/bin/env python3
"""Lightweight UI/UX Pro Max search helper for Codex.

Provides domain search and design-system generation compatible with the
UI/UX Pro Max workflow when the npm installer cannot fetch bundled assets.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent

MAX_RESULTS = 3
DOMAINS = {
    "style": [
        {"name": "Minimalism / Swiss", "best_for": "enterprise, dashboards, documentation", "guidance": "tight grid, strong whitespace, restrained palette, clear hierarchy"},
        {"name": "Glassmorphism", "best_for": "modern SaaS, finance, AI tools", "guidance": "blurred surfaces, translucent panels, subtle borders; maintain contrast"},
        {"name": "Bento Grid", "best_for": "feature showcases, portfolios, dashboards", "guidance": "modular cards, varied spans, one clear focal card, consistent gutters"},
        {"name": "Neubrutalism", "best_for": "Gen Z brands, creative tools", "guidance": "bold borders, offset shadows, saturated accents, simple typography"},
        {"name": "AI-Native UI", "best_for": "chatbots, copilots, automation", "guidance": "conversation-first layout, explainable states, trust cues, avoid generic purple gradients"},
    ],
    "color": [
        {"name": "SaaS Trust", "palette": "#2563EB primary, #0F172A text, #F8FAFC surface, #22C55E success", "best_for": "B2B SaaS and dashboards"},
        {"name": "Fintech Secure", "palette": "#0F766E primary, #111827 text, #ECFDF5 surface, #F59E0B warning", "best_for": "banking, insurance, crypto with restraint"},
        {"name": "Wellness Calm", "palette": "#A7C7A1 primary, #2D3436 text, #FFF7ED surface, #D4AF37 premium accent", "best_for": "spa, health, lifestyle"},
        {"name": "Creative Energy", "palette": "#7C3AED primary, #FF6B6B accent, #111827 text, #F8FAFC surface", "best_for": "creator tools and portfolios"},
    ],
    "typography": [
        {"name": "Inter / Source Serif 4", "mood": "modern, readable, editorial", "use": "SaaS marketing with long-form credibility"},
        {"name": "Manrope / IBM Plex Sans", "mood": "technical, precise", "use": "developer tools and dashboards"},
        {"name": "Cormorant Garamond / Montserrat", "mood": "elegant, premium", "use": "luxury, wellness, beauty"},
        {"name": "Space Grotesk / Inter", "mood": "contemporary, AI-native", "use": "AI products and startup landing pages"},
    ],
    "chart": [
        {"name": "Line chart", "best_for": "trends over time", "guidance": "label axes, expose exact values on hover/tap, support keyboard summary"},
        {"name": "Bar chart", "best_for": "category comparison", "guidance": "sort deliberately, avoid 3D, use direct labels for small datasets"},
        {"name": "Funnel", "best_for": "conversion flows", "guidance": "show absolute counts plus percentages between steps"},
        {"name": "Heatmap", "best_for": "density and calendar patterns", "guidance": "include legend and non-color fallback"},
    ],
    "ux": [
        {"name": "Accessibility", "rule": "normal text contrast >= 4.5:1, visible focus, labels, alt text, keyboard support"},
        {"name": "Touch", "rule": "interactive targets >= 44x44px with at least 8px spacing"},
        {"name": "Forms", "rule": "visible labels, inline validation after blur, clear recovery path, aria-live for errors"},
        {"name": "Motion", "rule": "150-300ms transitions, transform/opacity only, prefers-reduced-motion support"},
        {"name": "Responsive", "rule": "mobile first, no horizontal scroll, readable 16px body text, safe-area padding"},
    ],
    "product": [
        {"name": "SaaS", "pattern": "hero -> proof -> feature bento -> workflow -> pricing -> FAQ", "style": "Minimalism, Bento, AI-Native"},
        {"name": "E-commerce", "pattern": "value prop -> categories -> best sellers -> trust -> reviews -> checkout CTA", "style": "clean product-led UI"},
        {"name": "Healthcare", "pattern": "trust -> services -> credentials -> booking -> patient guidance", "style": "accessible calm minimalism"},
        {"name": "Portfolio", "pattern": "statement -> selected work -> process -> testimonials -> contact", "style": "editorial or kinetic typography"},
    ],
    "landing": [
        {"name": "Hero-centric", "sections": "hero, social proof, benefits, CTA", "best_for": "simple products with one strong promise"},
        {"name": "Problem-solution", "sections": "pain, stakes, solution, proof, pricing", "best_for": "B2B conversion"},
        {"name": "Feature bento", "sections": "hero, bento grid, integrations, testimonials, FAQ", "best_for": "SaaS and AI tools"},
    ],
    "google-fonts": [
        {"name": "Inter", "category": "sans", "use": "default UI font with broad language support"},
        {"name": "Manrope", "category": "sans", "use": "modern technical interfaces"},
        {"name": "Source Serif 4", "category": "serif", "use": "editorial trust and long-form content"},
    ],
    "prompt": [
        {"name": "Professional polish", "prompt": "Use semantic tokens, restrained palette, accessible contrast, clear hierarchy, and complete states."},
        {"name": "Avoid AI generic", "prompt": "Avoid default purple/pink gradients, random glass cards, emoji icons, and inconsistent shadows."},
    ],
}
STACKS = {
    "react": ["memoize expensive lists only after profiling", "split by route with Suspense/dynamic imports", "use semantic components and accessible form controls"],
    "nextjs": ["optimize images with next/image", "keep server/client boundaries intentional", "stream slow sections with skeletons"],
    "html-tailwind": ["use tokenized Tailwind classes", "container max widths and mobile-first breakpoints", "focus-visible rings on all controls"],
    "shadcn": ["compose accessible primitives", "centralize theme tokens", "preserve Radix keyboard behavior"],
    "react-native": ["respect safe areas", "minimum 44pt touch targets", "use FlatList virtualization for long lists"],
    "flutter": ["use Material 3 color roles", "support text scaling", "avoid rebuilding heavy widgets unnecessarily"],
    "swiftui": ["use Dynamic Type", "safe-area-aware navigation", "standard gestures and haptics"],
}


def score(query: str, item: dict[str, str]) -> int:
    words = set(query.lower().replace("/", " ").replace("-", " ").split())
    haystack = " ".join(str(v).lower() for v in item.values())
    return sum(1 for word in words if word in haystack)


def search(query: str, domain: str | None, max_results: int) -> dict:
    selected_domain = domain or "ux"
    rows = DOMAINS.get(selected_domain, [])
    ranked = sorted(rows, key=lambda item: score(query, item), reverse=True)[:max_results]
    return {"domain": selected_domain, "query": query, "count": len(ranked), "results": ranked}


def search_stack(query: str, stack: str, max_results: int) -> dict:
    rows = [{"guideline": value} for value in STACKS.get(stack, [])][:max_results]
    return {"stack": stack, "query": query, "count": len(rows), "results": rows}


def infer_product(query: str) -> dict:
    ranked = sorted(DOMAINS["product"], key=lambda item: score(query, item), reverse=True)
    return ranked[0]


def generate_design_system(query: str, project_name: str | None, fmt: str) -> str:
    product = infer_product(query)
    style = sorted(DOMAINS["style"], key=lambda item: score(query + " " + product["style"], item), reverse=True)[0]
    color = sorted(DOMAINS["color"], key=lambda item: score(query + " " + product["name"], item), reverse=True)[0]
    typo = sorted(DOMAINS["typography"], key=lambda item: score(query + " " + product["name"], item), reverse=True)[0]
    title = project_name or "Project"
    if fmt == "markdown":
        return dedent(f"""
        # {title} Design System

        - **Product pattern:** {product['pattern']}
        - **Recommended style:** {style['name']} — {style['guidance']}
        - **Color palette:** {color['name']} — {color['palette']}
        - **Typography:** {typo['name']} — {typo['mood']}; best use: {typo['use']}
        - **Core effects:** subtle elevation, clear focus rings, purposeful 150-300ms motion, skeleton loading.
        - **Avoid:** low contrast, tiny tap targets, generic AI gradients, emoji icons, inconsistent spacing, layout shift.
        """).strip()
    return dedent(f"""
    +------------------------------------------------------------+
    | {title.upper()} - RECOMMENDED DESIGN SYSTEM
    +------------------------------------------------------------+
    Product Pattern: {product['pattern']}
    Style: {style['name']} - {style['guidance']}
    Colors: {color['name']} - {color['palette']}
    Typography: {typo['name']} - {typo['mood']} ({typo['use']})
    Effects: subtle elevation, visible focus, 150-300ms purposeful motion.
    Avoid: low contrast, tiny tap targets, generic AI gradients, emoji icons, CLS.
    +------------------------------------------------------------+
    """).strip()


def persist(content: str, project_name: str | None, page: str | None, output_dir: str | None) -> None:
    slug = (project_name or "default").lower().replace(" ", "-")
    root = Path(output_dir or ".") / "design-system" / slug
    root.mkdir(parents=True, exist_ok=True)
    (root / "MASTER.md").write_text(content + "\n", encoding="utf-8")
    if page:
        pages = root / "pages"
        pages.mkdir(exist_ok=True)
        (pages / f"{page.lower().replace(' ', '-')}.md").write_text(content + "\n", encoding="utf-8")


def format_output(result: dict) -> str:
    header = "Stack" if "stack" in result else "Domain"
    key = result.get("stack") or result.get("domain")
    lines = [f"## UI/UX Pro Max Search Results", f"**{header}:** {key} | **Query:** {result['query']}", f"**Found:** {result['count']} results", ""]
    for index, row in enumerate(result["results"], 1):
        lines.append(f"### Result {index}")
        for field, value in row.items():
            lines.append(f"- **{field}:** {value}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="UI/UX Pro Max Search")
    parser.add_argument("query")
    parser.add_argument("--domain", "-d", choices=sorted(DOMAINS))
    parser.add_argument("--stack", "-s", choices=sorted(STACKS))
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--design-system", "-ds", action="store_true")
    parser.add_argument("--project-name", "-p")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii")
    parser.add_argument("--persist", action="store_true")
    parser.add_argument("--page")
    parser.add_argument("--output-dir", "-o")
    args = parser.parse_args()

    if args.design_system:
        output = generate_design_system(args.query, args.project_name, args.format)
        print(output)
        if args.persist:
            persist(output, args.project_name, args.page, args.output_dir)
        return

    result = search_stack(args.query, args.stack, args.max_results) if args.stack else search(args.query, args.domain, args.max_results)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else format_output(result))


if __name__ == "__main__":
    main()
