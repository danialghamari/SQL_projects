'''
    Creating a list of books
    The fields are .
'''
from books_async_funcs import get_book_urls,get_book_details
import os, pickle as pkl, asyncio


# ---------------------------------------------------------------------
async def batch_requests(urls, which_func,savefile_template):
    
    saving_rate = 50
    max_count = int(len(urls)/saving_rate)+1 if len(urls)%saving_rate!=0 else int(len(urls)/saving_rate)

    tasks = []
    for counter in range(max_count):
        start = counter * saving_rate
        end = (counter + 1) * saving_rate
        tasks.append(\
            asyncio.create_task(which_func(urls[start:end], savefile = f'{savefile_template}_{start}_{end}.pkl'))) 

    for counter,task in enumerate(asyncio.as_completed(tasks)):
        await task        
        print(f'{(counter + 1) * saving_rate}/{len(urls)} of "{which_func.__name__}"\'s tasks are done')





if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    
    # urls = [
    #     f"https://www.alistofbooks.com/?page={page}" for page in range(1,200+1)
    # ]
    
    # asyncio.run(batch_requests(urls=urls,
    #                            which_func=get_book_urls,
    #                            savefile_template=cur_dir+'/book_urls'))
    
    # list_files = [os.path.join(cur_dir,i) for i in os.listdir(cur_dir) if 'book_urls_' in i]
    # book_urls = pkl.load(open(list_files[0],'rb'))

    # for file in list_files[1:]:
    #     book_urls+=pkl.load(open(file,'rb'))

    # pkl.dump(book_urls,open(os.path.join(cur_dir,'book_urls.pkl'),'wb'))

    # for file in list_files: os.system('rm -f '+file)

    book_urls = pkl.load(open(os.path.join(cur_dir,'book_urls.pkl'),'rb'))
    
    asyncio.run(batch_requests(urls=book_urls,
                               which_func=get_book_details,
                               savefile_template=cur_dir+'/book_details'))
    
    list_files = [os.path.join(cur_dir,i) for i in os.listdir(cur_dir) if 'book_details_' in i]
    book_details = pkl.load(open(list_files[0],'rb'))

    for file in list_files[1:]:
        book_details+=pkl.load(open(file,'rb'))

    pkl.dump(book_details,open(os.path.join(cur_dir,'book_details.pkl'),'wb'))

    # for file in list_files: os.system('rm -f '+file)
