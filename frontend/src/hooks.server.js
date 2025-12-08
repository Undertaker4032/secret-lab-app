/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
    if (event.url.pathname === '/.well-known/traffic-advice') {
        return new Response(JSON.stringify({
            traffic_advice: {
                proxy: {
                    url_prefix: 'https://yourdomain.com/'
                }
            }
        }), {
            headers: { 'Content-Type': 'application/json' }
        });
    }
    
    const response = await resolve(event, {
        filterSerializedResponseHeaders: (name) => name === 'content-type',
    });
    
    return response;
}

/** @type {import('@sveltejs/kit').HandleServerError} */
export function handleError({ error, event }) {
    const errorMessage = error instanceof Error ? error.message : String(error);
    const errorStack = error instanceof Error ? error.stack : undefined;
    
    // Check if the error is a "Not found" 404 error
    if (errorMessage.includes('Not found')) {
        const ignoredPatterns = [
            '/wp-', '/admin', '/.env', '/.git',
            '/well-known', '/xmlrpc.php', '/favicon.ico',
            '/cgi-bin/', '/sitemap.xml', '/owa/',
            '/stalker_portal/', '/sendgrid.env',
            '/autodiscover/', '/ecp/'
        ];
        
        const shouldIgnore = ignoredPatterns.some(pattern => 
            event.url.pathname.includes(pattern)
        );
        
        if (shouldIgnore) {
            return new Error('Not Found');
        }
    }
    
    console.error('Server Error:', errorStack || errorMessage || 'Unknown error');
    
    return new Error('An unexpected error occurred');
}