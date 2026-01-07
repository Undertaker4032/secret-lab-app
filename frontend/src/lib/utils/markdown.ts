import { marked } from 'marked';
import { gfmHeadingId } from 'marked-gfm-heading-id';
import DOMPurify from 'dompurify';

marked.use(gfmHeadingId());
marked.setOptions({
  breaks: true,
  gfm: true,
  async: false,
});

export function markdownToHtml(markdown: string): string {
  if (!markdown) return '';
  
  try {
    const html = marked.parse(markdown) as string;
    
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'hr', 'pre', 'code', 'blockquote',
        'ul', 'ol', 'li', 'strong', 'em', 'del',
        'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'div', 'span', 'sup', 'sub'
      ],
      ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'class', 'id', 'target', 'rel'],
      ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto|ftp):|[^a-z]|[a-z+.-]+(?:[^a-z+.-:]|$))/i
    });
  } catch (error) {
    console.error('Error converting markdown:', error);
    return markdown;
  }
}

export function getTableOfContents(html: string): Array<{ id: string; text: string; level: number }> {
  if (!html) return [];
  
  try {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const headings = doc.querySelectorAll('h1, h2, h3, h4, h5, h6');
    const toc: Array<{ id: string; text: string; level: number }> = [];

    headings.forEach((heading) => {
      const id = heading.id;
      const text = heading.textContent || '';
      
      if (id && text.trim()) {
        toc.push({
          id: id,
          text: text,
          level: parseInt(heading.tagName.charAt(1))
        });
      }
    });

    return toc;
  } catch (error) {
    console.error('Error generating table of contents:', error);
    return [];
  }
}