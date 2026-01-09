import Image from "next/image";
import FileUploadPage from "./components/file";
import ChatPage from "./components/chat";
export default function Home() {
  return (
  <div>
    <div className="min-h-screen min-w-screen flex">
      <div className="w-[30vw] flex justify-center items-center min-h-screen"><FileUploadPage/></div>
      <div className="w-[70vw] min-h-screen border-l-2"><ChatPage/></div>
    </div>
  </div>
  );
}
