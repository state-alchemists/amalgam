<script lang="ts">
    import axios from 'axios';
	import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
	import { ensureAccessToken, getAuthorization } from '$lib/auth/helper';
    import { getErrorMessage } from '$lib/error/helper';

    export let data: {id?: string} = {};

    let row: any = {}
    let isAlertVisible: boolean = false;
    let isSaving: boolean = false;
    let errorMessage: string = '';
    let allowUpdate: boolean = false;

    onMount(async() => {
        await loadAuthorization();
        if (!allowUpdate) {
            goto('/');
        }
        await loadRow();
    });

    async function loadAuthorization() {
        const authorization = await getAuthorization([
            'library:book:update',
        ]);
        allowUpdate = authorization['library:book:update'] || false;
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

    async function onSaveClick() {
        isSaving = true
        const accessToken = await ensureAccessToken();
        try {
            const response = await axios.put(
                `/api/v1/library/books/${data.id}`, row, {headers: {Authorization: `Bearer ${accessToken}`}}
            );
            if (response?.status == 200) {
                errorMessage = '';
                isAlertVisible = false;
                await goto('../../');
                return;
            }
            errorMessage = 'Unknown error';
            isAlertVisible = true;
        } catch(error) {
            console.error(error);
            errorMessage = getErrorMessage(error);
            isAlertVisible = true;
        }
        isSaving = false;
    }
</script>

<h1 class="text-3xl">Book</h1>

<form class="max-w-md mx-auto bg-gray-100 p-6 rounded-md mt-5 mb-5">
  <h2 class="text-xl font-bold mb-4">Update Book</h2>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="code">Human zrb readable column name</label>
        <input type="text" class="input w-full" id="code" placeholder="Code" bind:value={row.code} />
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="title">Title</label>
        <input type="text" class="input w-full" id="title" placeholder="Title" bind:value="{row.title}" />
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="page-number">Page number</label>
        <input type="number" class="input w-full" id="page-number" placeholder="Page number" bind:value="{row.page_number}" />
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="purchase-date">Purchase date</label>
        <input type="date" class="input w-full" id="purchase-date" placeholder="Purchase date" bind:value="{row.purchase_date}" />
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="available">Available</label>
        <input type="checkbox" class="checkbox" id="available" bind:checked="{row.available}" />
    </div>
    <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="synopsis">Synopsis</label>
        <textarea class="textarea w-full" id="synopsis" placeholder="Synopsis" bind:value="{row.synopsis}"></textarea>
    </div>
    <!-- DON'T DELETE: insert new field here-->
    <a href="#top" class="btn btn-primary {isSaving ? 'btn-disabled': '' }" on:click={onSaveClick}>Save</a>
    <a href="../../" class="btn">Cancel</a>

    <div class="alert alert-error shadow-lg mt-5 {isAlertVisible? 'visible': 'hidden'}">
        <div>
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>{errorMessage}</span>
        </div>
    </div>

</form>