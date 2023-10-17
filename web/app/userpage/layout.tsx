import '../globals.css';

import ProvidersWrapper from './ProvidersWrapper';

export default async function UserPageLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
  <>
    <ProvidersWrapper>
      {children}
    </ProvidersWrapper>
  </>
  );
}