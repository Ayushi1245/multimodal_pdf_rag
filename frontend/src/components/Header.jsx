export default function Header() {
  return (
    <header className="flex justify-between items-center px-lg h-16 bg-surface border-b border-outline-variant/20 z-10 sticky top-0 shrink-0">
      <div className="flex-1 max-w-md hidden md:block">
        <div className="bg-surface-container-lowest flex items-center px-3 py-1.5 rounded-lg w-full border border-outline-variant/30 shadow-sm focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all">
          <span className="material-symbols-outlined text-on-surface-variant text-[20px] mr-2">search</span>
          <input className="bg-transparent border-none outline-none text-sm text-on-surface w-full placeholder:text-on-surface-variant focus:ring-0 p-0" placeholder="Search documents..." type="text" />
        </div>
      </div>

      <button className="md:hidden text-on-surface-variant p-sm rounded-full hover:bg-surface-container-high transition-colors">
        <span className="material-symbols-outlined" data-icon="menu">menu</span>
      </button>

      <div className="flex items-center gap-sm ml-auto">
        <button className="text-on-surface-variant p-sm rounded-full hover:bg-surface-container-high hover:text-primary transition-colors cursor-pointer relative">
          <span className="material-symbols-outlined">notifications</span>
          <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full"></span>
        </button>
        <button className="text-on-surface-variant p-sm rounded-full hover:bg-surface-container-high hover:text-primary transition-colors cursor-pointer">
          <span className="material-symbols-outlined">settings</span>
        </button>
        <div className="w-8 h-8 rounded-full ml-sm overflow-hidden border border-outline-variant cursor-pointer hover:border-primary transition-colors">
          <img alt="User profile" className="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBHHcIRIDBGzWyxSGq6TCd0Ex9CwCBpAai8vucSvbfaOe_LGScOcuSZrvqAYxOnFi6S5UPKm1Fpqq5uJQO-2-_zF3m0vNjxqc2r6HffyBRYGr1QOS9V4rffmfs7ucU5Qh2DZehZ1uMmps7mRY6H3ZFloBMe5rXP9DSaBzj1-FRg7y9atqg2XnhivWCj7EUROo63-PuV8PP9JJ05d0zARdOx3rU2KgtuVVrhLHNxCvbh1fQfE9NMsJYsZJnpolmlvEI5Cozpi6u2Onc" />
        </div>
      </div>
    </header>
  );
}
