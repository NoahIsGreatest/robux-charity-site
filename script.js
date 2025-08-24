const qs = (s) => document.querySelector(s);
const onboarding = qs('#onboarding');
const login = qs('#login');
const nav = qs('#nav');
const dash = qs('#dashboard');


const displayUser = qs('#displayUser');
const balanceEl = qs('#balance');
const startBtn = qs('#startBtn');
const loginForm = qs('#loginForm');
const usernameInput = qs('#username');
const watchAdBtn = qs('#watchAd');
const grantBtn = qs('#grantBtn');
const withdrawAmount = qs('#withdrawAmount');
const withdrawBtn = qs('#withdrawBtn');


function show(el){ el.classList.remove('hidden'); el.classList.add('fade-in'); }
function hide(el){ el.classList.add('hidden'); }


async function me(){
try{
const r = await fetch('/api/me');
const j = await r.json();
return j.ok ? j : null;
}catch{
