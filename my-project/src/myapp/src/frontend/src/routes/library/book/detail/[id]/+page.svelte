<script lang="ts">
    import axios from 'axios';
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { ensureAccessToken, getAuthorization } from '$lib/auth/helper';
    import { getErrorMessage } from '$lib/error/helper';

    export let data: {id?: string} = {};

    let row: any = {};
    let isAlertVisible: boolean = false;
    let errorMessage: string = '';
    let allowGetById: boolean = false;
 
    onMount(async() => {
        await loadAuthorization();
        if (!allowGetById) {
            goto('/');
        }
        await loadRow();
    });

    async function loadAuthorization() {
        const authorization = await getAuthorization([
            'library:book:get_by_id',
        ]);
        allowGetById = authorization['library:book:get_by_id'] || false;
    }

    async function loadRow() {
        const accessToken = await ensureAccessToken();
        try {
            const response = await axios.get(
                `/api/v1/library/books/${data.id}`,
                {headers: {Authorization: `Bearer ${accessToken}`}}
            );
            if (response?.status == 200 && response?.data) {
                row = response.data;
                errorMessage = '';
                isAlertVisible = false;
                return;
            }
            errorMessage = 'Unknown error';
            isAlertVisible = true;
        } catch(error) {
            console.error(error);
            errorMessage = getErrorMessage(error);
            isAlertVisible = true;
        }
    }
</script>
<h1 class="text-3xl">Book</h1>

<form class="max-w-md mx-auto bg-gray-100 p-6 rounded-md mt-5 mb-5">
  <h2 class="text-xl font-bold mb-4">Show Book {data.id}</h2>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="code">Code</label>
        <span id="code">{row.code}</span>
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="title">Title</label>
        <span id="title">{row.title}</span>
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="page-number">Page number</label>
        <span id="page-number">{row.page_number}</span>
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="purchase-date">Purchase date</label>
        <span id="purchase-date">{row.purchase_date}</span>
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="available">Available</label>
        <span id="available">{row.available}</span>
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="synopsis">Synopsis</label>
        <span id="synopsis">{row.synopsis}</span>
    </div>
    <!-- DON'T DELETE: insert new field here-->
    <a href="../../" class="btn btn-primary">Show others</a>

    <div class="alert alert-error shadow-lg mt-5 {isAlertVisible? 'visible': 'hidden'}">
        <div>
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>{errorMessage}</span>
        </div>
    </div>

</form>