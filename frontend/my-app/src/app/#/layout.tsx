import { CPagination } from "@/components/pagination";
import { CButton } from "@/components/button";
import { PropsWithChildren } from "react";
import { Hotels } from "./hotels/page";

export default function Layout({ children }:
PropsWithChildren<unknown>) {
    return (
        <div>
            <Hotels/>
            <CButton/>
            <CPagination/>
        </div>
    )
}
